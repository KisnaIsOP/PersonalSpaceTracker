from datetime import datetime
import pytz

def format_datetime(dt_str, input_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    """Convert UTC datetime string to readable format"""
    try:
        dt = datetime.strptime(dt_str, input_format)
        dt = pytz.UTC.localize(dt)
        return dt.strftime("%B %d, %Y %H:%M UTC")
    except Exception:
        return dt_str

def calculate_distance_au_to_ly(au_distance):
    """Convert Astronomical Units (AU) to Light Years"""
    try:
        return float(au_distance) * 0.000015812507409
    except (ValueError, TypeError):
        return None

def format_number(number, decimal_places=2):
    """Format large numbers with comma separators and specified decimal places"""
    try:
        return f"{float(number):,.{decimal_places}f}"
    except (ValueError, TypeError):
        return "N/A"

def get_hazard_emoji(is_hazardous):
    """Return appropriate emoji based on hazard status"""
    return "⚠️" if is_hazardous else "✅"

def calculate_time_until(target_date_str):
    """Calculate time until a future event"""
    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        now = datetime.now(pytz.UTC)
        delta = target_date - now.replace(tzinfo=None)
        
        if delta.total_seconds() < 0:
            return "Past event"
        
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    except Exception:
        return "Invalid date"

def filter_launches(launches, start_date=None, end_date=None, organization=None):
    """Filter launches based on date range and organization"""
    filtered_launches = launches
    
    if start_date:
        filtered_launches = [
            l for l in filtered_launches 
            if datetime.strptime(l['date'], "%Y-%m-%dT%H:%M:%S.%fZ") >= start_date
        ]
    
    if end_date:
        filtered_launches = [
            l for l in filtered_launches 
            if datetime.strptime(l['date'], "%Y-%m-%dT%H:%M:%S.%fZ") <= end_date
        ]
    
    if organization:
        filtered_launches = [
            l for l in filtered_launches 
            if organization.lower() in l['name'].lower()
        ]
    
    return filtered_launches

def get_random_space_fact():
    """Return a random space fact"""
    facts = [
        "Light from the Sun takes about 8 minutes to reach Earth.",
        "One day on Venus is longer than its year.",
        "The footprints on the Moon will last for 100 million years.",
        "The largest known star, UY Scuti, is 1,700 times larger than our Sun.",
        "There are more stars in the universe than grains of sand on Earth.",
        "The International Space Station travels at about 17,500 mph.",
        "A year on Mercury is just 88 Earth days long.",
        "Jupiter's Great Red Spot is shrinking.",
        "Saturn's rings are mostly made of ice and rock.",
        "There are more trees on Earth than stars in the Milky Way."
    ]
    from random import choice
    return choice(facts)
