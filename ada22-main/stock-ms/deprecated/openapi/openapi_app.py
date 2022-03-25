import logging
import connexion
from connexion.resolver import RestyResolver
from stocks.deprecated.db import Base, engine

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir="openapi/")
app.add_api('stock-service-api.yaml',
            arguments={'title': 'Stock Service API'})
Base.metadata.create_all(engine)
app.run(host='0.0.0.0', port=5000, debug=True)