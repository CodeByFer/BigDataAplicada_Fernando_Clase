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