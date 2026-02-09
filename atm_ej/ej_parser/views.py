# from django.shortcuts import render

# # Create your views here.

import os
import re
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_http_methods

from .parser.ej_splitter import split_transactions
from .parser.transaction_builder import build_transaction
from .parser.mongo import db


# -------------------------------------------------
# Upload Page (GET)
# -------------------------------------------------
def upload_page(request):
    """
    Render EJ upload UI
    """
    return render(request, 'upload.html')


# -------------------------------------------------
# Upload + Parse EJ File (POST)
# -------------------------------------------------
@require_http_methods(["POST"])
def upload_ej(request):
    """
    Handle EJ file upload, parse content, store transactions
    """
    ej_file = request.FILES.get('ej_file')

    # ---------- Validation ----------
    if not ej_file:
        return render(request, 'upload.html', {
            'error': 'No file selected'
        })

    ext = os.path.splitext(ej_file.name)[1].lower()
    if ext not in ['.txt', '.log', '.csv']:
        return render(request, 'upload.html', {
            'error': 'Invalid file type'
        })

    if ej_file.size > 10 * 1024 * 1024:
        return render(request, 'upload.html', {
            'error': 'File exceeds 10MB limit'
        })

    # ---------- Save File ----------
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'ej_files'))
    filename = fs.save(ej_file.name, ej_file)
    file_path = fs.path(filename)

    # ---------- Read EJ Content ----------
    # with open(file_path, 'r', errors='ignore') as f:
    #     ej_text = f.read()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        ej_text = f.read()


    # ---------- Split into Transactions ----------
    transaction_blocks = split_transactions(ej_text)

    parsed_transactions = []

    for block in transaction_blocks:
        txn_data = build_transaction(block)
        if txn_data:
            parsed_transactions.append(txn_data)


   
    txn_collection = db["transactions"]
    txn_collection.delete_many({})

    if parsed_transactions:
        txn_collection.insert_many(parsed_transactions)

    # ---------- Redirect to Dashboard ----------
    return redirect('/dashboard/')
