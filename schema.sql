CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT UNIQUE,
    region TEXT NOT NULL,
    pin TEXT NOT NULL,
    position TEXT,
    is_blocked INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    specialty TEXT,
    organization TEXT,
    phone TEXT,
    address TEXT,
    latitude REAL,
    longitude REAL,
    region TEXT,
    category TEXT,
    notes TEXT,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS pharmacies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    network TEXT,
    address TEXT,
    phone TEXT,
    latitude REAL,
    longitude REAL,
    pharmacist_name TEXT,
    category TEXT,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS distributors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    contact_person TEXT,
    position TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    latitude REAL,
    longitude REAL,
    category TEXT
);

CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    visit_type TEXT NOT NULL,
    target_id INTEGER,
    target_name TEXT,
    visit_date TEXT NOT NULL,
    duration INTEGER,
    topics TEXT,
    result TEXT,
    products_presented TEXT,
    orders_received TEXT,
    latitude REAL,
    longitude REAL,
    location_verified INTEGER DEFAULT 0,
    photo_url TEXT,
    notes TEXT,
    next_visit_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS visit_reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    target_type TEXT NOT NULL,
    target_id INTEGER NOT NULL,
    last_visit_date TEXT,
    recommended_visit_date TEXT,
    reminder_sent INTEGER DEFAULT 0,
    priority TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
