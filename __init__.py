# This file is part account_invoice_shop module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import invoice
from . import sale


def register():
    Pool.register(
        invoice.Invoice,
        sale.Sale,
        module='account_invoice_shop', type_='model')
