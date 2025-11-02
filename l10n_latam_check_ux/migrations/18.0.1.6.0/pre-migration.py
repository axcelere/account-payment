from odoo import SUPERUSER_ID, api
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Eliminar cualquier vista que tenga el campo regimenes_ganancias_ids en su definición arch
    env['l10n_latam.check'].search([('payment_date', '=', False)]).write({'payment_date': fields.Date.today()})
    env.cr.commit()
