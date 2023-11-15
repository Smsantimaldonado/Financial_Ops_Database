SELECT Ticker,
	   (SELECT (sum((ValorNeto/Fx))/sum(Cantidad))*100
	   FROM OPERACIONES
	   WHERE Ticker='GD30' AND Tipo='Compra') as PPC_USD,
	   (SELECT (sum((ValorNeto/Fx))/sum(Cantidad))*100
	   FROM OPERACIONES
	   WHERE Ticker='GD30' AND Tipo='Venta') as PPV_USD
FROM OPERACIONES
WHERE Ticker='GD30'
LIMIT 1;