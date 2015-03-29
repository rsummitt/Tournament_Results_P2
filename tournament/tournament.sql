-- Player information
CREATE TABLE players (
  player_id           SERIAL PRIMARY KEY,
  player_name         VARCHAR(50),
  wins                INTEGER DEFAULT 0,
  losses              INTEGER DEFAULT 0,
  draws               INTEGER DEFAULT 0,
  received_bye        BOOLEAN DEFAULT FALSE
);

-- Tournament information
CREATE TABLE tournaments (
  tournament_id   SERIAL PRIMARY KEY,
  tournament_name VARCHAR(50)
);

-- Match information
CREATE TABLE matches (
  match_id      SERIAL PRIMARY KEY,
  tournament_id INTEGER REFERENCES tournaments (tournament_id) ON DELETE CASCADE
);

-- Junction table that associates many match results to matches and players
CREATE TABLE match_results (
  match_result_id SERIAL PRIMARY KEY,
  match_id        INTEGER REFERENCES matches (match_id) ON DELETE CASCADE,
  player_id       INTEGER REFERENCES players (player_id) ON DELETE CASCADE,
  result          VARCHAR(4) CHECK (result IN ('win', 'loss', 'draw')) ,
  CONSTRAINT match_results_fk UNIQUE (match_id, player_id)
);

-- Junction table that associates many players to many tournaments
CREATE TABLE tournament_players (
  player_id     INTEGER REFERENCES players (player_id) ON DELETE CASCADE,
  tournament_id INTEGER REFERENCES tournaments (tournament_id) ON DELETE CASCADE,
  PRIMARY KEY (player_id, tournament_id)
);

