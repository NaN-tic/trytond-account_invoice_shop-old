# This file is part account_invoice_shop module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Bool, Eval

__all__ = ['Invoice']


class Invoice:
    __metaclass__ = PoolMeta
    __name__ = 'account.invoice'
    shop = fields.Many2One('sale.shop', 'Shop', domain=[
            ('id', 'in', Eval('context', {}).get('shops', [])),
        ], states={
            'readonly': (Eval('state') != 'draft') | Bool(Eval('number')),
            'invisible': (Eval('type') == 'in'),
        }, depends=['reference', 'state', 'type'])
    shop_address = fields.Function(fields.Many2One('party.address',
        'Shop Address'), 'on_change_with_shop_address')

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        cls.currency.states['readonly'] |= Eval('shop')
        cls.currency.depends.append('shop')

    @staticmethod
    def default_company():
        User = Pool().get('res.user')

        user = User(Transaction().user)
        return user.shop.company.id if user.shop else \
            Transaction().context.get('company')

    @staticmethod
    def default_shop():
        User = Pool().get('res.user')

        user = User(Transaction().user)
        return user.shop.id if user.shop else None

    @fields.depends('shop', 'party')
    def on_change_shop(self):
        if not self.shop:
            return
        for fname in ('company', 'currency', 'payment_term'):
            fvalue = getattr(self.shop, fname)
            if fvalue:
                setattr(self, fname, fvalue.id)

    @fields.depends('shop')
    def on_change_with_shop_address(self, name=None):
        return (self.shop and self.shop.address and
            self.shop.address.id or None)
