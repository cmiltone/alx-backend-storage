-- script ranks country origins of bands, ordered by the number of (non-unique) fans
SELECT origin, COUNT(DISTINCT fans) AS nb_fans
ORDER BY fans;
