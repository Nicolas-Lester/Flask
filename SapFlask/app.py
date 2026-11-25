from flask import Flask, render_template
from flask_migrate import Migrate
from forms import PersonaForm
from models import Persona
from database import db

app = Flask(__name__)

#configuracion de la bd
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# #Inicializacion del objeto db de sqlalchemy
# db = SQLAlchemy(db)
db.init_app(app)

#configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#configuracion de flask-wtf
app.config['SECRET_KEY']='llave_secreta'
    
@app.route('/')
@app.route('/index.html')
def inicio():
    # Listado de personas
    personas = Persona.query.all()
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)

@app.route('/ver/<int:id>')
def ver_detalle(id):
    #Recperamos la persona segun el id proporcionado
    # persona = Persona.query.get(id)
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona = persona)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    persona = Persona()
    personaForm = PersonaForm(obj=persona)
