create database caos_news;

use caos_news;

INSERT INTO core_newsstate (state) VALUES 
('aprobado')
,('pendiente')
,('rechazado')
,('obsoleto');

INSERT INTO core_newscategory (category) VALUES
('nacional')
,('internacional')
,('economía')
,('deportes')
,('tendencias')
,('opinión');