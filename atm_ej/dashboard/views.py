# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from datetime import datetime
import csv
from ej_parser.parser.mongo import db
from pymongo import MongoClient
from django.http import HttpResponse


def dashboard_home(request):
    return render(request, 'dashboard.html')

def transaction_list(request):
    """
    Show Transaction Logs Table
    """
    # txn_collection = db["transactions"]

    # search_query = request.GET.get("q", "").strip()
    # status_filter = request.GET.get("status", "all").lower()
    # export = request.GET.get("export")

    # query = {}

    # # Status filter
    # if status_filter != "all":
    #     query["status"] = status_filter.upper()

    # # Search filter
    # if search_query:
    #     query["$or"] = [
    #         {"date": {"$regex": search_query, "$options": "i"}},
    #         {"card_no": {"$regex": search_query, "$options": "i"}},
    #         {"terminal_id": {"$regex": search_query, "$options": "i"}},
    #         {"txn_type": {"$regex": search_query, "$options": "i"}},
    #     ]

    # transactions = list(txn_collection.find(
    #     query, 
    #     {
    #         "_id": 0,
    #         "date": 1,
    #             "time": 1,
    #             "card_no": 1,
    #             "terminal_id": 1,
    #             "txn_type": 1,
    #             "amount": 1,
    #             "status": 1,
         
    #     }
    #     ))


    # # ✅ Sort using combined date + time
    # def sort_key(txn):
    #     try:
    #         return datetime.strptime(
    #             f"{txn.get('date')} {txn.get('time')}",
    #             "%d/%m/%y %H:%M:%S"
    #         )
    #     except Exception:
    #         return datetime.min

    # transactions.sort(key=sort_key, reverse=True)  # latest first

    # # -----------------------------
    # # EXPORT CSV
    # # -----------------------------
    # if export == "csv":
    #     response = HttpResponse(content_type="text/csv")
    #     response["Content-Disposition"] = 'attachment; filename="transactions.csv"'

    #     writer = csv.writer(response)
    #     writer.writerow([
    #         "Date", "Time", "Card No", "ATM ID", "Type", "Amount", "Status"
    #     ])

    #     for txn in transactions:
    #         writer.writerow([
    #             txn.get("date"),
    #             txn.get("time"),
    #             txn.get("card_no"),
    #             txn.get("terminal_id"),
    #             txn.get("txn_type"),
    #             txn.get("amount"),
    #             txn.get("status"),
    #         ])

    #     return response

    # # Counts (for UI)
    # # -----------------------------
    # total_count = txn_collection.count_documents({})
    # filtered_count = len(transactions)

    # return render(request, 'table.html', {
    #     "transactions": transactions,
    #     "total_count": total_count,
    #     "filtered_count": filtered_count,
    #     "search_query": search_query,
    #     "status_filter": status_filter,
    # })
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
    return render(request, 'errors.html')

def reconciliation_report(request):
    return render(request, 'reconciliation.html')

def cash_audit(request):
    return render(request, 'cash_audit.html')
