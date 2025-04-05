# populate_db.py
from app import app, db, Market, Dealer, CropInfo, GovPolicy, HarvestingSuggestion
import json
from datetime import datetime, date

# Run this within app context
with app.app_context():
    # Add Markets
    markets = [
        Market(
            name="Azadpur Mandi",
            location="Delhi",
            contact="011-27691703",
            market_type="wholesale",
            products=json.dumps([
                {"name": "Potato", "price": "15-20/kg"},
                {"name": "Tomato", "price": "25-30/kg"},
                {"name": "Onion", "price": "18-24/kg"}
            ])
        ),
        Market(
            name="Vashi APMC",
            location="Navi Mumbai",
            contact="022-27887236",
            market_type="wholesale",
            products=json.dumps([
                {"name": "Rice", "price": "35-40/kg"},
                {"name": "Wheat", "price": "28-32/kg"},
                {"name": "Pulses", "price": "80-120/kg"}
            ])
        ),
        Market(
            name="Gultekdi Market",
            location="Pune",
            contact="020-24261955",
            market_type="wholesale",
            products=json.dumps([
                {"name": "Grapes", "price": "60-80/kg"},
                {"name": "Pomegranate", "price": "100-140/kg"},
                {"name": "Banana", "price": "30-40/dozen"}
            ])
        )
    ]
    
    # Add Dealers
    dealers = [
        Dealer(
            name="Agro Solutions",
            location="Nagpur",
            contact="9876543210",
            dealer_type="fertilizer",
            products=json.dumps([
                {"name": "Urea", "price": "300/bag", "quantity": "50kg"},
                {"name": "DAP", "price": "1200/bag", "quantity": "50kg"},
                {"name": "Potash", "price": "800/bag", "quantity": "50kg"}
            ])
        ),
        Dealer(
            name="KisanBeej",
            location="Pune",
            contact="9876123450",
            dealer_type="seeds",
            products=json.dumps([
                {"name": "Wheat Seeds", "price": "60/kg", "variety": "HD-2967"},
                {"name": "Rice Seeds", "price": "75/kg", "variety": "Basmati-1121"},
                {"name": "Cotton Seeds", "price": "850/packet", "variety": "Bt Cotton"}
            ])
        ),
        Dealer(
            name="Farm Equipments Ltd",
            location="Chandigarh",
            contact="9870123456",
            dealer_type="equipment",
            products=json.dumps([
                {"name": "Tractor", "price": "550000-750000", "brand": "Mahindra"},
                {"name": "Thresher", "price": "35000-50000", "type": "Multi-crop"},
                {"name": "Sprayer", "price": "3000-8000", "capacity": "16L"}
            ])
        )
    ]
    
    # Add Crops
    crops = [
        CropInfo(
            name="Wheat",
            season="Rabi",
            duration=120,
            water_requirements="450-650mm",
            soil_type="Loamy",
            fertilizers=json.dumps([
                {"name": "Urea", "quantity": "120kg/hectare"},
                {"name": "DAP", "quantity": "60kg/hectare"},
                {"name": "Potash", "quantity": "40kg/hectare"}
            ]),
            pesticides=json.dumps([
                {"name": "Propiconazole", "target": "Leaf Rust"},
                {"name": "Chlorpyrifos", "target": "Aphids"}
            ]),
            expected_yield="4-5 tonnes/hectare"
        ),
        CropInfo(
            name="Rice",
            season="Kharif",
            duration=135,
            water_requirements="1000-1200mm",
            soil_type="Clay",
            fertilizers=json.dumps([
                {"name": "Urea", "quantity": "150kg/hectare"},
                {"name": "DAP", "quantity": "70kg/hectare"},
                {"name": "Zinc sulphate", "quantity": "25kg/hectare"}
            ]),
            pesticides=json.dumps([
                {"name": "Carbofuran", "target": "Stem borer"},
                {"name": "Tricyclazole", "target": "Blast"}
            ]),
            expected_yield="5-6 tonnes/hectare"
        ),
        CropInfo(
            name="Cotton",
            season="Kharif",
            duration=160,
            water_requirements="700-1200mm",
            soil_type="Black soil",
            fertilizers=json.dumps([
                {"name": "Urea", "quantity": "80kg/hectare"},
                {"name": "DAP", "quantity": "50kg/hectare"},
                {"name": "Potash", "quantity": "50kg/hectare"}
            ]),
            pesticides=json.dumps([
                {"name": "Imidacloprid", "target": "Sucking pests"},
                {"name": "Profenofos", "target": "American Bollworm"}
            ]),
            expected_yield="20-25 quintals/hectare"
        )
    ]
    
    # Add Policies
    policies = [
        GovPolicy(
            title="PM-KISAN Scheme",
            description="Income support of Rs.6000 per year in three equal installments to farmer families.",
            eligibility="All small and marginal farmers with cultivable landholding.",
            benefits="Direct cash transfer of Rs.6000 per year.",
            documents_required="Aadhaar Card, Land Records, Bank Account Details",
            application_process="Apply through local agriculture office or online portal.",
            start_date=date(2019, 2, 1),
            end_date=date(2025, 12, 31)
        ),
        GovPolicy(
            title="Kisan Credit Card",
            description="Provides farmers with affordable credit for their cultivation needs.",
            eligibility="All farmers, sharecroppers, and tenant farmers.",
            benefits="Low interest rates, flexibility in use, crop insurance coverage.",
            documents_required="Photo ID, Land Records, Bank Account Details",
            application_process="Apply through local bank branches.",
            start_date=date(1998, 8, 1),
            end_date=date(2030, 12, 31)
        ),
        GovPolicy(
            title="Pradhan Mantri Fasal Bima Yojana",
            description="Crop insurance scheme to provide financial support to farmers suffering crop loss/damage.",
            eligibility="All farmers growing notified crops in notified areas.",
            benefits="Insurance coverage for crop failure due to natural calamities.",
            documents_required="Land Records, Bank Account, Aadhaar Card",
            application_process="Apply at the time of taking crop loan or through CSCs.",
            start_date=date(2016, 2, 18),
            end_date=date(2026, 3, 31)
        )
    ]
    
    # Add Suggestions
    suggestions = [
        HarvestingSuggestion(
            crop_id=1,  # Wheat
            title="Optimal Wheat Harvesting",
            description="Best practices for wheat harvesting to maximize yield and quality.",
            best_practices="Harvest when moisture content is 12-14%. Use combine harvesters for efficiency.",
            expected_profit="Rs.20,000-25,000 per acre",
            market_demand="High"
        ),
        HarvestingSuggestion(
            crop_id=2,  # Rice
            title="Rice Harvesting Techniques",
            description="Efficient rice harvesting methods for better grain quality.",
            best_practices="Harvest when 80% of grains turn golden yellow. Dry properly after harvesting.",
            expected_profit="Rs.25,000-30,000 per acre",
            market_demand="High"
        ),
        HarvestingSuggestion(
            crop_id=3,  # Cotton
            title="Cotton Picking Best Practices",
            description="Maximize cotton quality through proper picking techniques.",
            best_practices="Pick when bolls are fully open but not weathered. Avoid early morning picking when dew is present.",
            expected_profit="Rs.35,000-45,000 per acre",
            market_demand="Medium"
        )
    ]
    
    # Add all data to database
    db.session.add_all(markets)
    db.session.add_all(dealers)
    db.session.add_all(crops)
    db.session.add_all(policies)
    
    # Commit first to get IDs for crops
    db.session.commit()
    
    # Now add suggestions
    db.session.add_all(suggestions)
    db.session.commit()
    
    print("Database populated successfully!")