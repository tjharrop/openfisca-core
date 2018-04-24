from openfisca_core.scripts import detect_country_package, build_tax_benefit_system
from openfisca_web_api_preview.app import create_app

country_package = detect_country_package()
extensions = None

tax_benefit_system = build_tax_benefit_system(
    country_package_name = country_package,
    extensions = extensions,
    reforms = None
)

application = create_app(tax_benefit_system)
