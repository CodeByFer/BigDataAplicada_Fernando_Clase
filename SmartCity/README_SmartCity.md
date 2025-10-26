# Carga de entidades

### Utilicé Postman para enviar una petición POST /v2/entites



```json
##### Sensor Temperatura
{
  "id": "SensorTemperatura-1",
  "type": "SensorTemperatura",
  "time": {
    "type": "DateTime",
    "value": "2026-03-02T00:00:00Z"
  },
  "temperatureValue": {
    "type": "Float",
    "value": 23
  },
  "temperatureMagnitude": {
    "type": "Text",
    "value": "C"
  },
  "humidityValue": {
    "type": "Float",
    "value": 23
  },
  "humidityMagnitude": {
    "type": "Text",
    "value": "g/m³"
  }
}

```


```json
##### Sensor CO2

{
  "id": "SensorCO2",
  "type": "SensorCO2",
  "time": {
    "type": "DateTime",
    "value": "2026-03-02T00:00:00Z"
  },
  "CO2_volume": {
    "type": "Float",
    "value": 23
  },
  "CO2_magnitude": {
    "type": "Text",
    "value": "ppm"
  }
}
```

```json
##### Sensor Agua

{
  "id": "SensorAgua",
  "type": "SensorAgua",
  "time": {
    "type": "DateTime",
    "value": "2026-03-02T00:00:00Z"
  },
  "ph": {
    "type": "Float",
    "value": 23
  },
  "chlorineVolume": {
    "type": "Float",
    "value": 23
  },
  "chlorineMagnitude": {
    "type": "Text",
    "value": "mgL"
  },
  "temperatureValue": {
    "type": "Float",
    "value": 23
  },
  "temperatureMagnitude": {
    "type": "Text",
    "value": "C"
  }
}
```


### Para crear las suscripciones hice lo mismo

```json
{
  "description": "Suscripcion para historico de Sensores Smart City",
  "subject": {
    "entities": [
      {
        "idPattern": ".*",
        "typePattern": "Sensor.*"
      }
    ],
    "condition": {
      "attrs": [
        "temperatureValue",
        "humidityValue",
        "CO2_volume",
        "ph",
        "chlorineVolume"
      ]
    }
  },
  "notification": {
    "http": {
      "url": "http://quantumleap:8668/v2/notify"
    },
    "attrsFormat": "normalized"
  }
}
```

### Carga de datos
Una vez todo creado, utilizamos un script python para la carga de datos a modo de simulación

```python
import requests
import random
import time
import json

# URL de la API de Orion
ORION_URL = "http://localhost:1026/v2/entities/"
HEADERS = {'Content-Type': 'application/json'}

entities_to_update = {
    "SensorTemperatura-1": ["temperatureValue", "humidityValue"],
    "SensorCO2": ["CO2_volume"],
    "SensorAgua": ["ph", "chlorineVolume", "temperatureValue"]
}


N_UPDATES = 400

print(f"--- Iniciando carga masiva de {N_UPDATES} actualizaciones por entidad ---")

for entity_id, attributes in entities_to_update.items():
    print(f"\nActualizando entidad: {entity_id}")
  
    entity_url = f"{ORION_URL}{entity_id}/attrs"
    
    for i in range(N_UPDATES):
       
        payload = {}
        
      
        if "temperatureValue" in attributes:
            payload["temperatureValue"] = { "value": round(random.uniform(15.0, 30.0), 2) }
        
        if "humidityValue" in attributes:
            payload["humidityValue"] = { "value": round(random.uniform(30.0, 60.0), 2) }
            
        if "CO2_volume" in attributes:
            payload["CO2_volume"] = { "value": round(random.uniform(400.0, 1500.0), 2) }
            
        if "ph" in attributes:
            payload["ph"] = { "value": round(random.uniform(6.5, 8.0), 2) }
            
        if "chlorineVolume" in attributes:
            payload["chlorineVolume"] = { "value": round(random.uniform(0.5, 2.0), 2) }

        
        try:
          
            response = requests.patch(entity_url, data=json.dumps(payload), headers=HEADERS)
            
            if response.status_code == 204:
               
                print(f"  {entity_id}: Update {i+1}/{N_UPDATES} ... OK")
            else:
                print(f"  {entity_id}: Update {i+1}/{N_UPDATES} ... Error {response.status_code}")
                print(response.text)
                
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            
       
        time.sleep(0.05)

print("\n--- Carga de datos completada ---")
```

