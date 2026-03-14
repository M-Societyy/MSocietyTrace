# MSocietyTrace - Herramienta de Social Tracking mediante WebRTC

> MSocietyTrace es una herramienta Flask para obtener información geolocalizada de usuarios mediante técnicas de WebRTC y fallback a IP remota.

## ¿Qué es MSocietyTrace?

MSocietyTrace es una herramienta de pentesting y seguridad diseñada para obtener información detallada sobre usuarios que visitan una página web. Utiliza técnicas avanzadas de WebRTC para descubrir la IP real de los usuarios (incluso cuando usan VPNs o proxies) y luego obtiene información geolocalizada precisa.

## ⚡ **Funciones Avanzadas Exclusivas**

### 🛡️ **Detección Avanzada de VPN/Proxy/Tor**
- **Análisis de ISP/Organización** para detectar proveedores VPN
- **Base de datos de hosting providers** (AWS, Azure, GCP, DigitalOcean, etc.)
- **Detección de Tor Browser** y nodos de salida
- **Sistema de puntuación de confianza** (0-100%)
- **Razones detalladas** de detección

### 🔍 **Fingerprinting Avanzado del Navegador**
- **Detección de bots y crawlers** automatizados
- **Análisis de privacidad** (bajo/medio/alto)
- **Hash único de fingerprint** para identificación
- **Detección de dispositivos móviles vs desktop**
- **Identificación exacta de navegador y versión**

### 💻 **Detección de Hardware**
- **Información GPU** (vendor y renderer)
- **Resolución de pantalla** y profundidad de color
- **WebGL support** y capacidades gráficas
- **Canvas fingerprinting** único
- **Hardware score** (puntuación de capacidades)

### 🌐 **Análisis de Red**
- **Tipo de conexión** (WiFi, móvil, cableada)
- **Ancho de banda efectivo** y latencia
- **Calidad de red** evaluada
- **Detección de redes móviles**
- **Análisis de rendimiento**

### 📊 **Exportación de Datos**
- **Auto-exportación JSON** con timestamp
- **Exportación CSV** para análisis
- **API endpoints** para exportación programática
- **Datos completos** con metadata

### 🖥️ **Panel de Control Web**
- **Dashboard en tiempo real** en `/dashboard`
- **Estadísticas generales** (total targets, VPNs, bots, móviles)
- **Tarjetas de target** con información completa
- **Indicadores visuales** de VPN/proxy/bot
- **Auto-refresh** cada 30 segundos

### 🎯 **Características Técnicas Únicas**

#### **Recopilación de Datos Avanzada**
- **Screen fingerprinting**: resolución, color depth, pixel ratio
- **WebGL rendering**: GPU vendor y renderer
- **Canvas fingerprinting**: hash único del canvas
- **Network API**: tipo de conexión, bandwidth, RTT
- **Performance timing**: métricas de carga
- **Timezone detection**: zona horaria real
- **Language detection**: idioma del navegador

#### **Análisis Inteligente**
- **Cross-reference analysis**: correlación de múltiples fuentes
- **Confidence scoring**: sistema de puntuación avanzado
- **Pattern recognition**: detección de patrones sospechosos
- **Historial de sesiones**: tracking por session ID

#### **Funciones de Seguridad**
- **Headers de seguridad** completos
- **CORS configurado** para acceso controlado
- **Sin persistencia** de datos sensibles
- **Validación de datos** integral

### Descubrimiento de IP
- **WebRTC IP Discovery**: Utiliza múltiples servidores STUN para obtener la IP real del cliente
- **Fallback a IP Remota**: Si WebRTC falla (TOR, bloqueo UDP), usa la IP de la petición HTTP
- **Soporte Dual Stack**: Detección de direcciones IPv4 e IPv6

### Geolocalización Avanzada
- **Múltiples APIs Geolocalización**: 
  - `ip-api.com` (Recomendado)
  - `ipapi.co`
- **Información Detallada**:
  - País, Región, Ciudad
  - Coordenadas (latitud, longitud)
  - Código postal
  - ISP y ASN
  - Información de conexión

### Funcionalidades de Engaño Social
- **Personalización de Página**: Título e imagen para social engineering
- **Open Graph Tags**: Previsualización personalizada en redes sociales
- **Interfaz Minimalista**: Diseño simple para no levantar sospechas

### Tunneling y Acceso Remoto
- **Cloudflared**: Tunelización mediante Cloudflare (recomendado)
- **Serveo.net**: Alternativa de tunelización SSH
- **URL Pública Automática**: Generación automática de URL accesible públicamente

### Recolección de Información del Cliente
- **User Agent**: Navegador y versión detallada
- **Plataforma**: Sistema operativo y arquitectura
- **Información del Navegador**: Versión, vendor, plataforma
- **Fallback Inteligente**: Cambio automático si WebRTC falla

## Instalación

### Prerrequisitos
- Python 3.7+
- SSH (para serveo.net)
- Cloudflared (opcional pero recomendado)

### Pasos de Instalación
```bash
# Clonar el repositorio
git clone https://github.com/M-Societyy/MSocietyTrace.git
cd MSocietyTrace

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o venv\Scripts\activate  # Windows

# Instalar dependencias
pip3 install -r requirements.txt
```

### Instalar Cloudflared (Opcional)
```bash
# Linux/Mac
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# O descargar desde: https://github.com/cloudflare/cloudflared/releases/
```

## Uso y Casos de Aplicación

### Ejecución Rápida
```bash
# Opción 1: Usar el launcher completo (recomendado)
./run.sh

# Opción 2: Ejecución rápida directa
./quick_run.sh

# Opción 3: Manual
python3 index.py
```

### Scripts de Ejecución

#### 🚀 **run.sh** (Launcher Completo)
- **Verificación automática** de dependencias
- **Creación de entorno virtual** si no existe
- **Instalación automática** de requirements.txt
- **Verificación de herramientas** del sistema
- **Banners profesionales** y mensajes informativos
- **Manejo de errores** con instrucciones claras

#### ⚡ **quick_run.sh** (Ejecución Rápida)
- **Ejecución directa** sin verificaciones
- **Para usuarios avanzados**
- **Asumiendo entorno ya configurado**

### Configuración Interactiva
Al ejecutar la herramienta, te pedirá configurar:

1. **URL de Imagen**: Para previsualización en redes sociales
2. **Título de Página**: Título que mostrará el navegador
3. **Puerto Local**: Puerto para el servidor Flask (ej: 8080)
4. **API de Geolocalización**: Elegir entre ip-api.com o ipapi.co
5. **Servicio de Tunneling**: Cloudflared o serveo.net

### Casos de Uso Legítimos

#### Testing de Seguridad
- **Verificación de VPNs**: Comprobar si las VPN realmente ocultan la IP
- **Testing de TOR**: Validar la efectividad de conexiones TOR
- **Auditoría de WebRTC**: Evaluar filtraciones de IP en aplicaciones web

#### Educación y Concienciación
- **Demostraciones de Seguridad**: Mostrar riesgos de WebRTC
- **Training de Ciberseguridad**: Enseñar sobre filtraciones de información
- **Research Académico**: Estudios sobre privacidad en navegadores

#### Corporate Security
- **Testing de Empleados**: Verificar políticas de seguridad
- **Phishing Ethics**: Demostraciones de seguridad corporativa
- **Red Team Operations**: Herramienta para simulaciones

## Funcionamiento Técnico

### Flujo de WebRTC
1. **Conexión STUN**: El cliente se conecta a múltiples servidores STUN
2. **ICE Candidates**: Se obtienen candidatos de conexión con IPs reales
3. **Extracción de IP**: Se parsean los candidatos para obtener IPv4/IPv6
4. **Envío al Servidor**: La información se envía vía POST al servidor

### Proceso de Fallback
```python
# Si WebRTC falla:
if request.form.get("is_rtc") != "true":
    # Usar IP remota de la petición HTTP
    ip = request.remote_addr
    # Indicar posible uso de TOR/bloqueo UDP
```

### Servidores STUN Utilizados
- `stun:stun.l.google.com:19302`
- `stun:stun.antisip.com:3478`
- `stun:stun.arbuz.ru:3478`
- `stun:stun.avigora.com:3478`
- Y más servidores redundantes

## Información Recopilada

### Datos del Cliente
- **IP Real** (IPv4/IPv6)
- **User Agent Completo**
- **Plataforma/OS**
- **Versión del Navegador**
- **Vendor del Navegador**

### Datos Geolocalizados
- **País** y **Región**
- **Ciudad** y **Código Postal**
- **Coordenadas** (Lat/Lon)
- **ISP** y **ASN**
- **Tipo de Conexión**

## Consideraciones de Seguridad

### Aspectos Técnicos
- **Headers de Seguridad**: Implementa X-Frame-Options, XSS Protection
- **CORS Configurado**: Control de acceso entre orígenes
- **Sin Persistencia**: No almacena datos permanentemente

### Limitaciones Conocidas
- **TOR Users**: WebRTC falla, usa IP de salida TOR
- **Bloqueo UDP**: Clientes que bloquean tráfico UDP/STUN
- **Navegadores Seguros**: Algunos navegadores bloquean WebRTC

## Advertencia Legal y Ética

**IMPORTANTE**: Esta herramienta está diseñada exclusivamente para:

✅ **Propósitos Educativos**  
✅ **Testing de Seguridad Autorizado**  
✅ **Research Legítimo**  
✅ **Demostraciones de Concienciación**  

**NO USAR PARA**:
❌ Ciberacoso o stalking  
❌ Actividades ilegales  
❌ Violación de privacidad  
❌ Acoso digital  

**Uso Responsable**: 
- Solo en redes que owns o con permiso explícito
- Para educación y testing ético
- Cumpliendo leyes locales y regulaciones

## Troubleshooting

### Problemas Comunes

#### Cloudflared no funciona
```bash
# Verificar instalación
which cloudflared
# Reinstalar si es necesario
```

#### WebRTC no detecta IPs
- **Causa**: Cliente usa TOR, bloqueo UDP, navegador seguro
- **Solución**: La herramienta hace fallback automático a IP remota

#### Error de Puerto
```bash
# Verificar puerto disponible
netstat -tulpn | grep :8080
# Elegir otro puerto (ej: 8081, 3000, 9000)
```

### Debug Mode
Para ver logs detallados, comenta la línea:
```python
log.disabled = True  # Línea 25 en index.py
```

## Contribuciones

Las contribuciones son bienvenidas para:
- Nuevas APIs de geolocalización
- Mejoras en la interfaz
- Nuevos métodos de detección
- Documentación mejorada

## Licencia

Este proyecto es para fines educativos y de seguridad. Úsalo responsablemente.

---

**Desarrollado por**: c1q_ , Cyk, M-Society Developers Team  
**Categoría**: Herramienta de Social Tracking y Educación en Seguridad  
**Nivel**: principiante 

Signed by M-Society.
