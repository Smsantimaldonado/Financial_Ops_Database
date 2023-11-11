SELECT
    Ticker,
    ((SUM(CASE WHEN tipo = 'Compra' THEN cantidad ELSE 0 END))
	-
    (SUM(CASE WHEN tipo = 'Venta' THEN cantidad ELSE 0 END))) AS Tenencias
FROM
    OPERACIONES
WHERE
    Clase IN ('Equity', 'Bonos', 'ONs', 'Crypto')
GROUP BY
    Ticker
HAVING
    Tenencias > 0
ORDER BY
    Tenencias DESC;
