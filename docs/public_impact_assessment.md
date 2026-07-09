<div align="center">

<img src="../RECURSOS/presentation/assets/logo.png" alt="Sanghelios" width="300">

# Evaluación de impacto público

**Beneficios, riesgos éticos y mitigación de sesgos**

[README](../README.md) · [Planteamiento](planteamiento_problema.md) · [Marco metodológico](marco_metodologico.md) · [Validación](validación_guide.md)

</div>

---

## Beneficio público

Anticipar la escasez de sangre con 14 días de ventaja permite al Hospital
General de Medellín pasar de campañas **reactivas** (cuando la sangre ya falta)
a campañas **preventivas**, reduciendo el riesgo de cancelación de cirugías y
de desabastecimiento para pacientes crónicos. El sistema completo se construyó
sobre **datos abiertos** de [datos.gov.co](https://www.datos.gov.co) y se
publica con licencia abierta, por lo que cualquier banco de sangre del país
puede replicarlo.

## Privacidad y gobernanza de datos

| Aspecto | Cómo se maneja |
|---|---|
| **Fuente** | Conjuntos ya anonimizados por el HGM antes de su publicación en datos.gov.co (sin nombres, documentos ni direcciones exactas) |
| **Nivel de agregación** | El modelo predictivo consume únicamente **series diarias agregadas** (conteos de donaciones, hospitalizaciones y defunciones); ninguna predicción se hace sobre personas |
| **Datos generados** | Los flyers personalizados usan datos que la persona ingresa voluntariamente y no se persisten fuera de la sesión |
| **Credenciales** | `GEMINI_API_KEY` vive en `.env` (no versionado); políticas en [`config/security_policy.json`](../config/security_policy.json) |

## Riesgos identificados y mitigación

| Riesgo | Mitigación |
|---|---|
| **Falso negativo** (no alertar una escasez real) es el error más costoso | Umbral de decisión optimizado con **F2**, que penaliza más perder alertas que emitir falsas alarmas; el dashboard muestra siempre la presión real junto a la predicción para supervisión humana |
| **Sesgo de segmentación** en campañas (excluir grupos de donantes) | El EDA mostró que la **edad es el único eje** que separa donantes; la segmentación cambia el *canal*, nunca el mensaje ni la elegibilidad. Pruebas automatizadas en [`tests/bias_tests/`](../tests/bias_tests/) verifican que el modelo no use atributos sensibles |
| **Contenido generativo** (Gemini) con errores o tono inadecuado | El asistente propone, el humano dispone: toda campaña es editable en vivo antes de publicarse y existe un generador por reglas como respaldo sin IA |
| **Sobreconfianza en un modelo modesto** | Las limitaciones se documentan explícitamente en [conclusiones.md](conclusiones.md); la señal del modelo se presenta como apoyo a la decisión, no como sustituto |

## Equidad algorítmica

El clasificador `escasez_t14` **no recibe ningún atributo demográfico**
(edad, sexo, grupo sanguíneo, comuna): sus 50 features son transformaciones de
tres series temporales agregadas. Esto se verifica de forma automatizada en
[`tests/bias_tests/test_equidad.py`](../tests/bias_tests/test_equidad.py),
que falla si una variable sensible entra al conjunto de features del modelo
publicado.

---

<div align="center"><sub>Sanghelios · Hospital General de Medellín · 2026</sub></div>
