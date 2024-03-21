import pandas as pd
import json
import piigenerator

def main():
    config_path = 'config_file.json'
    archivo_nombres = 'name_variant_hackathon.txt'
    excel_path = 'prueba.xlsx'
    
    # Cargar el archivo de configuración
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    # Cargar datos desde Excel antes de pasarlos a PiiGenerator
    seed_records = pd.read_excel(excel_path, header=0)

    # Crear la instancia de PiiGenerator
    generator = piigenerator.PiiGenerator(config, seed_records, archivo_nombres)
    records = generator.generate_records()
    
    # Procesar los records como necesites

if __name__ == "__main__":
    main()
