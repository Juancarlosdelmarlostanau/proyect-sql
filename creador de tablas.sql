CREATE DATABASE IF NOT EXISTS proyectomysql;
USE proyectomysql;

CREATE TABLE IF NOT EXISTS pais (
    id_pais VARCHAR(20) PRIMARY KEY,
    country VARCHAR(50),
    regional_indicator VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS ranking (
    id_pais VARCHAR(20) PRIMARY KEY,
    ranking INT,
    happiness_score DECIMAL(5,3),
    FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);

CREATE TABLE IF NOT EXISTS pib_bm (
    id_pais VARCHAR(20) PRIMARY KEY,
    pib DECIMAL(10,3),
    FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);

CREATE TABLE IF NOT EXISTS social (
    id_pais VARCHAR(20) PRIMARY KEY,
    social_support DECIMAL(10,3),
    freedom_to_make_life_choices DECIMAL(10,3),
    generosity DECIMAL(10,3),
    perceptions_of_corruption DECIMAL(10,3),
    FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);

CREATE TABLE IF NOT EXISTS infraestructura (
    id_pais VARCHAR(20) PRIMARY KEY,
    acceso_electrico DECIMAL(10,3),
    acceso_agua decimal (10,3),
    FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);