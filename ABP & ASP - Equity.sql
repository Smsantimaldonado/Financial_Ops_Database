SELECT Ticker,
	   (SELECT (sum((ValorNeto/Fx))/sum(Cantidad))
	   FROM OPERACIONES
	   WHERE Ticker='BABA' AND Tipo='Compra') as PPC_USD,
	   (SELECT (sum((ValorNeto/Fx))/sum(Cantidad))
	   FROM OPERACIONES
	   WHERE Ticker='BABA' AND Tipo='Venta') as PPV_USD
FROM OPERACIONES
WHERE Ticker='BABA'
LIMIT 1;
