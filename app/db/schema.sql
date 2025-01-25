CREATE TABLE IF NOT EXISTS clients (
  dni TEXT PRIMARY KEY,
  name TEXT,
  email TEXT,
  capital FLOAT
);

CREATE TABLE IF NOT EXISTS simulaciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dni TEXT,
  tae FLOAT,
  plazo INTEGER,
  cuota FLOAT,
  importe_total FLOAT,
  created_at TEXT,
  updated_at TEXT,
  FOREIGN KEY (dni) REFERENCES clients(dni)
);