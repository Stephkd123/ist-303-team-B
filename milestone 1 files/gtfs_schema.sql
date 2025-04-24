CREATE TABLE stops (
  stop_id TEXT PRIMARY KEY,
  stop_name TEXT,
  stop_desc TEXT,
  stop_lat REAL,
  stop_lon REAL
);

CREATE TABLE routes (
  route_id TEXT PRIMARY KEY,
  route_short_name TEXT,
  route_long_name TEXT,
  route_desc TEXT,
  route_type INTEGER
);

CREATE TABLE trips (
  route_id TEXT,
  service_id TEXT,
  trip_id TEXT PRIMARY KEY,
  trip_headsign TEXT,
  shape_id TEXT,
  FOREIGN KEY(route_id) REFERENCES routes(route_id)
);

CREATE TABLE stop_times (
  trip_id TEXT,
  arrival_time TEXT,
  departure_time TEXT,
  stop_id TEXT,
  stop_sequence INTEGER,
  pickup_type INTEGER,
  drop_off_type INTEGER,
  stop_headsign INTEGER,
  PRIMARY KEY (trip_id, stop_id),
  FOREIGN KEY(trip_id) REFERENCES trips(trip_id),
  FOREIGN KEY(stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE calendar(
  service_id TEXT PRIMARY KEY, 
  monday INTEGER, 
  tuesday INTEGER, 
  wednesday INTEGER, 
  thursday INTEGER, 
  friday INTEGER, 
  saturday INTEGER, 
  sunday INTEGER, 
  start_date INTEGER, 
  end_date INTEGER,
  FOREIGN KEY(service_id) REFERENCES trips(service_id)
);

CREATE TABLE agency(
  service_id TEXT PRIMARY KEY, 
  monday INTEGER, 
  tuesday INTEGER, 
  wednesday INTEGER, 
  thursday INTEGER, 
  friday INTEGER, 
  saturday INTEGER, 
  sunday INTEGER, 
  start_date INTEGER, 
  end_date INTEGER,
  FOREIGN KEY(service_id) REFERENCES trips(service_id)
);

CREATE TABLE shapes(
  shape_id TEXT PRIMARY KEY, 
  shape_pt_lat REAL, 
  shape_pt_lon REAL, 
  shape_pt_sequence INTEGER
);

CREATE TABLE transfers(
  from_stop_id TEXT, 
  to_stop_id TEXT, 
  transfer_type INTEGER
);
-- You’ll also need shapes, calendar, transfers, etc. as needed.
