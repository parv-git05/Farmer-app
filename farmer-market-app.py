# app.py - Main Flask application
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
import json
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmer_market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    location = db.Column(db.String(100))
    farmer_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Market(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    contact = db.Column(db.String(15))
    market_type = db.Column(db.String(50))  # wholesale, retail, etc.
    products = db.Column(db.Text)  # JSON string of products
    
class Dealer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    contact = db.Column(db.String(15))
    dealer_type = db.Column(db.String(50))  # fertilizer, seeds, equipment
    products = db.Column(db.Text)  # JSON string of products
    
class CropInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(50))
    duration = db.Column(db.Integer)  # days to harvest
    water_requirements = db.Column(db.String(100))
    soil_type = db.Column(db.String(100))
    fertilizers = db.Column(db.Text)  # JSON string
    pesticides = db.Column(db.Text)  # JSON string
    expected_yield = db.Column(db.String(50))
    
class GovPolicy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    benefits = db.Column(db.Text)
    documents_required = db.Column(db.Text)
    application_process = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
class HarvestingSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop_info.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    best_practices = db.Column(db.Text)
    expected_profit = db.Column(db.String(50))
    market_demand = db.Column(db.String(50))  # high, medium, low

# Create all tables
with app.app_context():
    db.create_all()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
# Change this line in your app.py
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    # It should be 'index.html', not 'F_template.html' or 'F_index.html'
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        location = request.form.get('location')
        farmer_type = request.form.get('farmer_type')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')
        
        user = User(username=username, name=name, phone=phone, 
                    location=location, farmer_type=farmer_type)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    # Get some sample data for dashboard
    markets = Market.query.limit(5).all()
    dealers = Dealer.query.limit(5).all()
    crops = CropInfo.query.limit(5).all()
    policies = GovPolicy.query.limit(3).all()
    
    return render_template('dashboard.html', 
                          user=user, 
                          markets=markets,
                          dealers=dealers,
                          crops=crops,
                          policies=policies)

@app.route('/markets')
@login_required
def markets():
    markets = Market.query.all()
    return render_template('markets.html', markets=markets)

# Add error handling for JSON parsing
@app.route('/market/<int:market_id>')
@login_required
def market_detail(market_id):
    market = Market.query.get_or_404(market_id)
    products = []
    if market.products:
        try:
            products = json.loads(market.products)
        except json.JSONDecodeError:
            products = []
    return render_template('market_detail.html', market=market, products=products)


@app.route('/dealers')
@login_required
def dealers():
    dealer_type = request.args.get('type', '')
    
    if dealer_type:
        dealers = Dealer.query.filter_by(dealer_type=dealer_type).all()
    else:
        dealers = Dealer.query.all()
        
    return render_template('dealers.html', dealers=dealers, current_type=dealer_type)

@app.route('/dealer/<int:dealer_id>')
@login_required
def dealer_detail(dealer_id):
    dealer = Dealer.query.get_or_404(dealer_id)
    products = []
    if dealer.products:
        try:
            products = json.loads(dealer.products)
        except json.JSONDecodeError:
            products = []
    return render_template('dealer_detail.html', dealer=dealer, products=products)

@app.route('/crops')
@login_required
def crops():
    season = request.args.get('season', '')
    
    if season:
        crops = CropInfo.query.filter_by(season=season).all()
    else:
        crops = CropInfo.query.all()
        
    return render_template('crops.html', crops=crops, current_season=season)

@app.route('/crop/<int:crop_id>')
@login_required
def crop_detail(crop_id):
    crop = CropInfo.query.get_or_404(crop_id)
    fertilizers = []
    pesticides = []
    if crop.fertilizers:
        try:
            fertilizers = json.loads(crop.fertilizers)
        except json.JSONDecodeError:
            fertilizers = []
    if crop.pesticides:
        try:
            pesticides = json.loads(crop.pesticides)
        except json.JSONDecodeError:
            pesticides = []
    suggestions = HarvestingSuggestion.query.filter_by(crop_id=crop_id).all()
    
    return render_template('crop_detail.html', 
                           crop=crop, 
                           fertilizers=fertilizers,
                           pesticides=pesticides,
                           suggestions=suggestions)

@app.route('/policies')
@login_required
def policies():
    policies = GovPolicy.query.all()
    return render_template('policies.html', policies=policies)

@app.route('/policy/<int:policy_id>')
@login_required
def policy_detail(policy_id):
    policy = GovPolicy.query.get_or_404(policy_id)
    return render_template('policy_detail.html', policy=policy)

@app.route('/suggestions')
@login_required
def suggestions():
    suggestions = HarvestingSuggestion.query.all()
    return render_template('suggestions.html', suggestions=suggestions)

@app.route('/suggestion/<int:suggestion_id>')
@login_required
def suggestion_detail(suggestion_id):
    suggestion = HarvestingSuggestion.query.get_or_404(suggestion_id)
    crop = CropInfo.query.get(suggestion.crop_id)
    return render_template('suggestion_detail.html', suggestion=suggestion, crop=crop)

# API Routes
@app.route('/api/markets')
def api_markets():
    markets = Market.query.all()
    result = []
    for market in markets:
        result.append({
            'id': market.id,
            'name': market.name,
            'location': market.location,
            'contact': market.contact,
            'market_type': market.market_type,
            'products': json.loads(market.products)
        })
    return jsonify(result)

@app.route('/api/dealers')
def api_dealers():
    dealers = Dealer.query.all()
    result = []
    for dealer in dealers:
        result.append({
            'id': dealer.id,
            'name': dealer.name,
            'location': dealer.location,
            'contact': dealer.contact,
            'dealer_type': dealer.dealer_type,
            'products': json.loads(dealer.products)
        })
    return jsonify(result)

@app.route('/api/crops')
def api_crops():
    crops = CropInfo.query.all()
    result = []
    for crop in crops:
        result.append({
            'id': crop.id,
            'name': crop.name,
            'season': crop.season,
            'duration': crop.duration,
            'water_requirements': crop.water_requirements,
            'soil_type': crop.soil_type,
            'fertilizers': json.loads(crop.fertilizers),
            'pesticides': json.loads(crop.pesticides),
            'expected_yield': crop.expected_yield
        })
    return jsonify(result)

@app.route('/api/policies')
def api_policies():
    policies = GovPolicy.query.all()
    result = []
    for policy in policies:
        result.append({
            'id': policy.id,
            'title': policy.title,
            'description': policy.description,
            'eligibility': policy.eligibility,
            'benefits': policy.benefits,
            'documents_required': policy.documents_required,
            'application_process': policy.application_process,
            'start_date': str(policy.start_date),
            'end_date': str(policy.end_date)
        })
    return jsonify(result)

@app.route('/api/suggestions')
def api_suggestions():
    suggestions = HarvestingSuggestion.query.all()
    result = []
    for suggestion in suggestions:
        result.append({
            'id': suggestion.id,
            'crop_id': suggestion.crop_id,
            'title': suggestion.title,
            'description': suggestion.description,
            'best_practices': suggestion.best_practices,
            'expected_profit': suggestion.expected_profit,
            'market_demand': suggestion.market_demand
        })
    return jsonify(result)

# Weather API integration (example)
@app.route('/weather')
@login_required
def weather():
    user = User.query.get(session['user_id'])
    location = request.args.get('location', user.location)
    
    # This is a placeholder for actual API call
    # You would need to register for a weather API service
    # Example with OpenWeatherMap
    # api_key = 'your_api_key'
    # url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    # response = requests.get(url)
    # data = response.json()
    
    # For demo purposes, we'll use mock data
    data = {
        'location': location,
        'temperature': 28,
        'condition': 'Sunny',
        'humidity': 65,
        'wind_speed': 12,
        'forecast': [
            {'day': 'Today', 'temp': 28, 'condition': 'Sunny'},
            {'day': 'Tomorrow', 'temp': 27, 'condition': 'Partly Cloudy'},
            {'day': 'Day 3', 'temp': 29, 'condition': 'Sunny'},
            {'day': 'Day 4', 'temp': 26, 'condition': 'Rain'},
            {'day': 'Day 5', 'temp': 25, 'condition': 'Rain'}
        ]
    }
    
    return render_template('weather.html', weather=data)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
