-- MySQL dump 10.13  Distrib 5.7.18, for osx10.12 (x86_64)
--
-- Host: ec2-54-89-211-122.compute-1.amazonaws.com    Database: SIMI
-- ------------------------------------------------------
-- Server version	5.5.54-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Importadores`
--

DROP TABLE IF EXISTS `Importadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Importadores` (
  `id_persona` bigint(20) NOT NULL,
  `descripcion_corta` varchar(58) DEFAULT NULL,
  `id_actividad` int(11) DEFAULT NULL,
  `desc_actividad` varchar(149) DEFAULT NULL,
  `mail` varchar(30) DEFAULT NULL,
  `area` int(11) DEFAULT NULL,
  `telefono` int(11) DEFAULT NULL,
  `fecha_hora_datos` varchar(19) DEFAULT NULL,
  `tiene_acuerdo_exp_imp` varchar(1) DEFAULT NULL,
  `tiene_acuerdo_precios` varchar(1) DEFAULT NULL,
  `acumulado_solicitado` int(11) DEFAULT NULL,
  `acumulado_procesado` int(11) DEFAULT NULL,
  `acumulado_pendiente` int(11) DEFAULT NULL,
  `acumulado_autorizado` int(11) DEFAULT NULL,
  `acumulado_observado` int(11) DEFAULT NULL,
  `porcentaje_pendiente` int(11) DEFAULT NULL,
  `porcentaje_procesado` int(11) DEFAULT NULL,
  `porcentaje_autorizado` int(11) DEFAULT NULL,
  `porcentaje_observado` int(11) DEFAULT NULL,
  `acumulado_cancelado` int(11) DEFAULT NULL,
  `porcentaje_cancelado` int(11) DEFAULT NULL,
  `total_importado_anio_anterior` int(11) DEFAULT NULL,
  `porcentaje_indicador_anio_actual` int(11) DEFAULT NULL,
  `monto_acuerdo_exp_imp` int(11) DEFAULT NULL,
  `id_grupo_importadores` varchar(30) DEFAULT NULL,
  `total_exportado_anio_anterior` int(11) DEFAULT NULL,
  `inversiones` int(11) DEFAULT NULL,
  `monto_referencia_anio_anterior` int(11) DEFAULT NULL,
  `fecha_acuerdo_firma` varchar(30) DEFAULT NULL,
  `fecha_acuerdo_desde` varchar(30) DEFAULT NULL,
  `fecha_acuerdo_hasta` varchar(30) DEFAULT NULL,
  `cantidad_meses_acuerdo` varchar(30) DEFAULT NULL,
  `acumulado_autorizado_acuerdo` int(11) DEFAULT NULL,
  `empleados_cantidad` int(11) DEFAULT NULL,
  `empleados_cantidad_fecha` varchar(19) DEFAULT NULL,
  `acumulado_fob_dolares_disponible_sali` int(11) DEFAULT NULL,
  `inversiones_rjai` int(11) DEFAULT NULL,
  `observaciones` varchar(15) DEFAULT NULL,
  `tiene_acuerdo_exp_imp_lna` varchar(1) DEFAULT NULL,
  `tiene_acuerdo_precios_lna` varchar(1) DEFAULT NULL,
  `acumulado_solicitado_lna` int(11) DEFAULT NULL,
  `acumulado_procesado_lna` int(11) DEFAULT NULL,
  `acumulado_pendiente_lna` int(11) DEFAULT NULL,
  `acumulado_autorizado_lna` int(11) DEFAULT NULL,
  `acumulado_observado_lna` int(11) DEFAULT NULL,
  `acumulado_cancelado_lna` int(11) DEFAULT NULL,
  `porcentaje_pendiente_lna` int(11) DEFAULT NULL,
  `porcentaje_procesado_lna` int(11) DEFAULT NULL,
  `porcentaje_autorizado_lna` int(11) DEFAULT NULL,
  `porcentaje_observado_lna` int(11) DEFAULT NULL,
  `porcentaje_cancelado_lna` int(11) DEFAULT NULL,
  `total_importado_anio_anterior_lna` int(11) DEFAULT NULL,
  `porcentaje_indicador_anio_actual_lna` int(11) DEFAULT NULL,
  `monto_acuerdo_exp_imp_lna` int(11) DEFAULT NULL,
  `total_exportado_anio_anterior_lna` int(11) DEFAULT NULL,
  `inversiones_lna` int(11) DEFAULT NULL,
  `monto_referencia_anio_anterior_lna` int(11) DEFAULT NULL,
  `fecha_acuerdo_firma_lna` varchar(19) DEFAULT NULL,
  `fecha_acuerdo_desde_lna` varchar(19) DEFAULT NULL,
  `fecha_acuerdo_hasta_lna` varchar(19) DEFAULT NULL,
  `cantidad_meses_acuerdo_lna` int(11) DEFAULT NULL,
  `acumulado_autorizado_acuerdo_lna` int(11) DEFAULT NULL,
  `acumulado_fob_dolares_disponible_sali_lna` int(11) DEFAULT NULL,
  `inversiones_rjai_lna` int(11) DEFAULT NULL,
  `importado_acum_lna_anio_actual` int(11) DEFAULT NULL,
  `importado_acum_lna_anio_anterior` int(11) DEFAULT NULL,
  `max_impo_auto_acum_lna` int(11) DEFAULT NULL,
  `monto_acuerdo_exp_imp_anio_proximo` int(11) DEFAULT NULL,
  `fecha_acuerdo_firma_anio_proximo` varchar(30) DEFAULT NULL,
  `fecha_vigencia_acuerdo_anio_proximo` varchar(30) DEFAULT NULL,
  `cantidad_meses_acuerdo_anio_proximo` varchar(30) DEFAULT NULL,
  `tipo_acuerdo_pos_aranc` varchar(30) DEFAULT NULL,
  `tipo_acuerdo_8_o_12` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id_persona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `a1dest`
--

DROP TABLE IF EXISTS `a1dest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `a1dest` (
  `id` int(11) NOT NULL,
  `destinacion` varchar(16) DEFAULT NULL,
  `estado` varchar(4) DEFAULT NULL,
  `fecha_ofic` varchar(19) DEFAULT NULL,
  `cuit_importador` bigint(20) DEFAULT NULL,
  `razon_social_importador` varchar(30) DEFAULT NULL,
  `cuit_despachante` bigint(20) DEFAULT NULL,
  `razon_social_despachante` varchar(30) DEFAULT NULL,
  `condicion_venta` varchar(30) DEFAULT NULL,
  `descripcion_condicion_venta` varchar(30) DEFAULT NULL,
  `moneda_fob` varchar(3) DEFAULT NULL,
  `descripcion_moneda_fob` varchar(20) DEFAULT NULL,
  `monto_fob` int(11) DEFAULT NULL,
  `moneda_flete` varchar(3) DEFAULT NULL,
  `descripcion_moneda_flete` varchar(20) DEFAULT NULL,
  `monto_flete` int(11) DEFAULT NULL,
  `moneda_seguro` varchar(3) DEFAULT NULL,
  `descripcion_moneda_seguro` varchar(20) DEFAULT NULL,
  `monto_seguro` int(11) DEFAULT NULL,
  `descripcion_bloqueo` varchar(30) DEFAULT NULL,
  `fecha_bloqueo` varchar(19) DEFAULT NULL,
  `numero_item` int(11) DEFAULT NULL,
  `pais_origen` int(11) DEFAULT NULL,
  `nombre_pais_origen` varchar(20) DEFAULT NULL,
  `unidad_medida_declarada` int(11) DEFAULT NULL,
  `descripcion_unidad_medida` varchar(14) DEFAULT NULL,
  `cantidad_unidades_declarada` int(11) DEFAULT NULL,
  `fob_dolares` int(11) DEFAULT NULL,
  `precio_unitario` int(11) DEFAULT NULL,
  `tiene_subitem` varchar(1) DEFAULT NULL,
  `numero_subitem` int(11) DEFAULT NULL,
  `fob_dolares_subitem` decimal(8,2) DEFAULT NULL,
  `cantidad_unidades_declarada_subitem` int(11) DEFAULT NULL,
  `precio_unitario_subitem` int(11) DEFAULT NULL,
  `motivo_bloqueo` varchar(4) DEFAULT NULL,
  `posicion_arancelaria` varchar(15) DEFAULT NULL,
  `descripcion_arancelaria` varchar(254) DEFAULT NULL,
  `fecha_arribo_item` varchar(19) DEFAULT NULL,
  `fecha_embarque_item` varchar(19) DEFAULT NULL,
  `pais_procedencia` int(11) DEFAULT NULL,
  `nombre_pais_procedencia` varchar(20) DEFAULT NULL,
  `estado_gestion` varchar(1) DEFAULT NULL,
  `descripcion_mercaderia` varchar(97) DEFAULT NULL,
  `codigo_actividad` int(11) DEFAULT NULL,
  `descripcion_actividad` varchar(110) DEFAULT NULL,
  `tramite_urgente` varchar(2) DEFAULT NULL,
  `fecha_envio_afip` varchar(23) DEFAULT NULL,
  `usuario_envio_afip` varchar(11) DEFAULT NULL,
  `fecha_ultima_modificacion` varchar(23) DEFAULT NULL,
  `usuario_ultima_modificacion` varchar(23) DEFAULT NULL,
  `tiene_acuerdo_exp_imp` varchar(1) DEFAULT NULL,
  `tiene_acuerdo_precios` varchar(1) DEFAULT NULL,
  `monto_acuerdo_exp_imp` int(11) DEFAULT NULL,
  `acumulado_solicitado` bigint(20) DEFAULT NULL,
  `acumulado_autorizado` bigint(20) DEFAULT NULL,
  `porcentaje_indicador_anio_actual` int(11) DEFAULT NULL,
  `id_grupo_importadores` varchar(30) DEFAULT NULL,
  `cantidad_disponible_item` int(11) DEFAULT NULL,
  `cantidad_disponible_subitem` int(11) DEFAULT NULL,
  `peso_neto_kg` int(11) NOT NULL,
  `unidad_estadistica` int(11) NOT NULL,
  `cant_estadistica` int(11) NOT NULL,
  `marca_item` varchar(12) DEFAULT NULL,
  `modelo_item` varchar(19) DEFAULT NULL,
  `version_item` varchar(30) DEFAULT NULL,
  `marca_subitem` varchar(11) DEFAULT NULL,
  `modelo_subitem` varchar(16) DEFAULT NULL,
  `version_subitem` varchar(30) DEFAULT NULL,
  `estado_gestion_bloqueo_bi45` varchar(30) DEFAULT NULL,
  `fecha_modificacion_bloqueo_bi45` varchar(30) DEFAULT NULL,
  `usuario_modificacion_bloqueo_bi45` varchar(30) DEFAULT NULL,
  `fecha_envio_afip_bloqueo_bi45` varchar(30) DEFAULT NULL,
  `usuario_envio_afip_bloqueo_bi45` varchar(30) DEFAULT NULL,
  `fecha_rectificacion_bloqueo_bi45` varchar(30) DEFAULT NULL,
  `usuario_rectificacion_bloqueo_bi45` varchar(30) DEFAULT NULL,
  `bloqueo_bi45` varchar(30) DEFAULT NULL,
  `lna` varchar(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `djais`
--

DROP TABLE IF EXISTS `djais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djais` (
  `destinacion` varchar(16) NOT NULL,
  `estado_djai` varchar(1) DEFAULT NULL,
  `fecha_envio_afip` varchar(23) DEFAULT NULL,
  `usuario_envio_afip` varchar(11) DEFAULT NULL,
  `fecha_ultima_modificacion` varchar(23) DEFAULT NULL,
  `usuario_ultima_modificacion` varchar(23) DEFAULT NULL,
  `numero_transaccion` int(11) DEFAULT NULL,
  `fecha_importacion` varchar(23) DEFAULT NULL,
  `cuit_importador` bigint(20) DEFAULT NULL,
  `razon_social_importador` varchar(30) DEFAULT NULL,
  `descripcion_actividad` varchar(133) DEFAULT NULL,
  `tramite_urgente` varchar(2) DEFAULT NULL,
  `codigo_actividad` int(11) DEFAULT NULL,
  `fob_dolares` int(11) DEFAULT NULL,
  `estado` varchar(4) DEFAULT NULL,
  `fecha_anulacion` varchar(19) DEFAULT NULL,
  `fecha_ultimo_envio_afip` varchar(23) DEFAULT NULL,
  `usuario_ultimo_envio_afip` varchar(11) DEFAULT NULL,
  `fecha_rectificacion` varchar(30) DEFAULT NULL,
  `usuario_rectificacion` varchar(30) DEFAULT NULL,
  `fecha_ofic` varchar(19) DEFAULT NULL,
  `fecha_salidas` varchar(30) DEFAULT NULL,
  `fecha_cancelaciones` varchar(30) DEFAULT NULL,
  `fecha_observaciones` varchar(19) DEFAULT NULL,
  `numero_transaccion_array_salida` varchar(30) DEFAULT NULL,
  `numero_transaccion_array_cancelado` varchar(30) DEFAULT NULL,
  `cancelado_zf` varchar(1) DEFAULT NULL,
  `inversiones` varchar(1) DEFAULT NULL,
  `giro_divisas` varchar(30) DEFAULT NULL,
  `plazo_giro_divisas` varchar(30) DEFAULT NULL,
  `plazo_giro_divisas_aux` varchar(30) DEFAULT NULL,
  `porcentaje_giro_divisas` varchar(30) DEFAULT NULL,
  `cotizacion_divisa` int(11) DEFAULT NULL,
  `anulacion_motivo` varchar(10) DEFAULT NULL,
  `fecha_caducidad` varchar(19) DEFAULT NULL,
  `fob_dolares_disponible` int(11) DEFAULT NULL,
  `moneda_fob` varchar(3) DEFAULT NULL,
  `numero_transaccion_array_prorroga` varchar(30) DEFAULT NULL,
  `vendedor` varchar(50) DEFAULT NULL,
  `clave_rjai` varchar(30) DEFAULT NULL,
  `fecha_ultima_rjai` varchar(30) DEFAULT NULL,
  `fecha_actualizacion_disponibles` varchar(30) DEFAULT NULL,
  `numero_transaccion_disponible` varchar(30) DEFAULT NULL,
  `cudap` varchar(20) DEFAULT NULL,
  `motivo_bloqueo` varchar(4) DEFAULT NULL,
  `fecha_bloqueo` varchar(19) DEFAULT NULL,
  `fob_dolares_bi34` int(11) DEFAULT NULL,
  `bloqueo_bi45` varchar(30) DEFAULT NULL,
  `usuario_rechazo` varchar(30) DEFAULT NULL,
  `fecha_rechazo` varchar(30) DEFAULT NULL,
  `fob_dolares_lna_disponible` int(11) DEFAULT NULL,
  `simi_escalonada` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`destinacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-28 10:00:59
