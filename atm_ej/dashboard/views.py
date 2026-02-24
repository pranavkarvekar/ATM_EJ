# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from datetime import datetime
import csv
from ej_parser.parser.mongo import db
from pymongo import MongoClient
from django.http import HttpResponse
from ej_parser.parser.reconciliation import reconcile_transactions

def dashboard_home(request):
    txn_collection = db["transactions"]

    total_txns = txn_collection.count_documents({})

    success_txns = txn_collection.count_documents({
        "status": "SUCCESS"
    })

    failed_txns = txn_collection.count_documents({
        "status": "FAILED"
    })

    # Sum of dispensed cash (SUCCESS only)
    cash_cursor = txn_collection.aggregate([
        {"$match": {"status": "SUCCESS"}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ])

    cash_result = list(cash_cursor)
    total_cash = cash_result[0]["total"] if cash_result else 0

    # Success rate
    success_rate = round((success_txns / total_txns) * 100, 2) if total_txns else 0
    error_rate = round((failed_txns / total_txns) * 100, 2) if total_txns else 0

    return render(request, "dashboard.html", {
        "total_txns": total_txns,
        "success_txns": success_txns,
        "failed_txns": failed_txns,
        "success_rate": success_rate,
        "error_rate": error_rate,
        "total_cash": int(total_cash)
    })

def transaction_list(request):
    """
    Show Transaction Logs Table
    """
   
    txn_collection = db["transactions"]

    # -----------------------------
    # GET PARAMS
    # -----------------------------
    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "all")
    export = request.GET.get("export")

    # -----------------------------
    # MONGODB QUERY
    # -----------------------------
    query = {}

    if status_filter != "all":
        query["status"] = status_filter.upper()

    if search_query:
        query["$or"] = [
            {"date": {"$regex": search_query, "$options": "i"}},
            {"time": {"$regex": search_query, "$options": "i"}},
            {"card_no": {"$regex": search_query, "$options": "i"}},
            {"terminal_id": {"$regex": search_query, "$options": "i"}},
            {"txn_type": {"$regex": search_query, "$options": "i"}},
        ]

    transactions = list(
        txn_collection.find(query, {"_id": 0})
    )

    # -----------------------------
    # EXPORT CSV (ONLY HERE)
    # -----------------------------
    if export == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Date", "Time", "Card No", "ATM ID", "Type", "Amount", "Status"
        ])

        for txn in transactions:
            writer.writerow([
                txn.get("date"),
                txn.get("time"),
                txn.get("card_no"),
                txn.get("terminal_id"),
                txn.get("txn_type"),
                txn.get("amount"),
                txn.get("status"),
            ])

        return response

    # -----------------------------
    # SORT (DATE + TIME)
    # -----------------------------
    def sort_key(txn):
        try:
            return datetime.strptime(
                f"{txn.get('date')} {txn.get('time')}",
                "%d/%m/%y %H:%M:%S"
            )
        except:
            return datetime.min

    transactions.sort(key=sort_key, reverse=True)

    # -----------------------------
    # RENDER TABLE
    # -----------------------------
    return render(request, "table.html", {
        "transactions": transactions,
        "search_query": search_query,
        "status_filter": status_filter,
        "total_count": txn_collection.count_documents({}),
        "filtered_count": len(transactions),
    })


def transaction_timeline(request, txn_id):
    return render(request, 'timeline.html', {'txn_id': txn_id})

def error_list(request):
    """
    Show Error Transactions
    """
    txn_collection = db["transactions"]

    errors = list(
        txn_collection.find(
            {
                "status": "FAILED",
                "$or": [
                    {"error_code": {"$exists": True}},
                    {"error_reason": {"$exists": True}}
                ]
            },
            {
                "_id": 0,
                "date": 1,
                "time": 1,
                "txn_type": 1,
                "terminal_id": 1,
                "amount": 1,
                "error_code": 1,
                "error_reason": 1
            }
        )
    )

    # ✅ Proper datetime sorting
    def sort_key(txn):
        try:
            return datetime.strptime(
                f"{txn.get('date')} {txn.get('time')}",
                "%d/%m/%y %H:%M:%S"
            )
        except:
            return datetime.min

    errors.sort(key=sort_key, reverse=True)

    return render(request, 'errors.html', {
        "errors": errors,
        "error_count": len(errors)
    })


# def reconciliation_report(request):
#     return render(request, 'reconciliation.html')
def reconciliation_report(request):

    txn_collection = db["transactions"]

    transactions = list(txn_collection.find({}))

    result = reconcile_transactions(transactions)

    return render(request, "reconciliation.html", result)

def cash_audit(request):
    txn_collection = db["transactions"]

    total_requested = 0.0
    total_dispensed = 0.0
    total_failed = 0.0
    phantom_risk = 0.0

    transactions = txn_collection.find(
        {},
        {
            "_id": 0,
            "amount": 1,
            "dispensed_amount": 1,
            "status": 1,
            "is_timeout": 1
        }
    )

    for txn in transactions:
        req = txn.get("amount") or 0
        disp = txn.get("dispensed_amount") or 0

        total_requested += req
        total_dispensed += disp

        if txn.get("status") == "FAILED":
            total_failed += req

        if txn.get("is_timeout"):
            phantom_risk += req

    audit_status = "BALANCED" if phantom_risk == 0 else "NOT BALANCED"

    return render(request, "cash_audit.html", {
        "total_requested": int(total_requested),
        "total_dispensed": int(total_dispensed),
        "total_failed": int(total_failed),
        "phantom_risk": int(phantom_risk),
        "audit_status": audit_status
    })


