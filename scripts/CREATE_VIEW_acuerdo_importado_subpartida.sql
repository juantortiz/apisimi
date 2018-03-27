--
CREATE OR REPLACE VIEW acuerdo_importado_subpartida AS
SELECT
    a.id,
    a.cuit,
    a.posicion_arancelaria,
    a.fob_cantidad,
    a.unidad_medida,
    a.factor_lineal,
    i.fob_dolares,
    i.cantidad,
    i.unidad_declarada,
    i.cantidad_disponible,
    i.fob_dolares_disponible,
    (
        a.fob_cantidad - GREATEST(
            (
                COALESCE(i.fob_dolares, 0)
                + GREATEST(
                    COALESCE(i.fob_dolares_disponible, 0)
                    , 0
                )
            )
            , COALESCE(i.fob_dolares_autorizado_vigente, 0)
        )
    ) AS libre_acuerdo,
    (
        a.fob_cantidad - GREATEST(
            (
                COALESCE(i.cantidad, 0)
                + GREATEST(
                    COALESCE(i.cantidad_disponible, 0)
                    , 0
                )
            )
            , COALESCE(i.cantidad_autorizado_vigente, 0)
        )
    ) AS libre_acuerdo_cantidad,
    a.tope_fob,
    i.cantidad_autorizado_vigente,
    i.fob_dolares_autorizado_vigente
FROM
	-- acuerdo_posicion_arancelaria a
	acuerdo_pa a
	LEFT JOIN importado_por_subpartida i
		ON (i.cuit = a.cuit)
		AND (a.posicion_arancelaria = i.subpartida)
;
--
