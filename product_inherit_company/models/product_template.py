#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = ["multi.company.abstract", "product.template"]
    _name = "product.template"

    company_ids = fields.Many2many(
        compute="_compute_company_ids",
        store=True,
        readonly=False,
    )

    @api.depends(
        "company_ids.parent_id",
    )
    def _compute_company_ids(self):
        for product in self:
            company = product.company_id

            # Get the oldest parent
            while company:
                parent_company = company.parent_id
                if parent_company:
                    company = parent_company
                    continue
                else:
                    # When `company` has no parent, it is the oldest parent
                    parent_company = company
                    break
            else:
                parent_company = company

            children_companies = self.env["res.company"].search(
                [
                    ("id", "child_of", parent_company.id),
                ],
            )

            product.company_ids = parent_company | children_companies
