{
    'name': "inventory_owner_transfer",
    'summary': "Manages ownership transfer of inventory items.",
    'description': """This module allows users to transfer ownership of inventory items from one consignor to another and provides reports on these transfers.""",
    'author': "Eyosiyas Mekbib",
    'category': 'Inventory',
    'version': '0.1',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/stock_ownership_transfer_log_views.xml',
        # 'views/owner_transfer_views.xml'
    ],
    'demo': [],
}
