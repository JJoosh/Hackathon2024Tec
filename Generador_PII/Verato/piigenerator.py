import pandas as pd
import random
from datetime import datetime, timedelta
from difflib import SequenceMatcher  # Para calcular la similitud entre cadenas


class PiiGenerator:
    def __init__(self, config, seed_records, archivos_nombres):

        self.current_id = 1
        self.config = config
        self.seed_records = seed_records  # Ahora ya contiene los datos, no necesitas cargarlos desde un archivo
        # self.seed_records = pd.read_excel(excel_path, header=0)  # Elimina o comenta esta línea
        self.nombres = self.cargar_datos_desde_txt(archivos_nombres)

        self.config = config

        print("Primera fila del Excel:", self.seed_records.iloc[0])


        if 'Date of Birth' not in self.seed_records.columns:
            raise ValueError("La clave 'Date of Birth' no está presente en la primera fila del archivo Excel.")
        print("Primera fila del Excel:", self.seed_records.iloc[0])

        self.area_codes = {
            "Alabama": ["205", "251", "256", "334", "659", "938"],
            "Alaska": ["907"],
            "Arizona": ["480", "520", "602", "623", "928"],
            "Arkansas": ["479", "501", "870"],
            "California": ["209", "213", "279", "310", "323", "341", "350", "408", "415", "424", "442", "510", "530", "559", "562", "619", "626", "628", "650", "657", "661", "669", "707", "714", "747", "760", "805", "818", "820", "831", "840", "858", "909", "916", "925", "949", "951"],
            "Colorado": ["303", "719", "720", "970", "983"],
            "Connecticut": ["203", "475", "860", "959"],
            "Delaware": ["302"],
            "Florida": ["239", "305", "321", "352", "386", "407", "448", "561", "656", "689", "727", "754", "772", "786", "813", "850", "863", "904", "941", "954"],
            "Georgia": ["229", "404", "470", "478", "678", "706", "762", "770", "912", "943"],
            "Hawaii": ["808"],
            "Idaho": ["208", "986"],
            "Illinois": ["217", "224", "309", "312", "331", "447", "464", "618", "630", "708", "773", "779", "815", "847", "872"],
            "Indiana": ["219", "260", "317", "463", "574", "765", "812", "930"],
            "Iowa": ["319", "515", "563", "641", "712"],
            "Kansas": ["316", "620", "785", "913"],
            "Kentucky": ["270", "364", "502", "606", "859"],
            "Louisiana": ["225", "318", "337", "504", "985"],
            "Maine": ["207"],
            "Maryland": ["240", "301", "410", "443", "667"],
            "Massachusetts": ["339", "351", "413", "508", "617", "774", "781", "857", "978"],
            "Michigan": ["231", "248", "269", "313", "517", "586", "616", "734", "810", "906", "947", "989"],
            "Minnesota": ["218", "320", "507", "612", "651", "763", "952"],
            "Mississippi": ["228", "601", "662", "769"],
            "Missouri": ["314", "417", "557", "573", "636", "660", "816"],
            "Montana": ["406"],
            "Nebraska": ["308", "402", "531"],
            "Nevada": ["702", "725", "775"],
            "New Hampshire": ["603"],
            "New Jersey": ["201", "551", "609", "640", "732", "848", "856", "862", "908", "973"],
            "New Mexico": ["505", "575"],
            "New York": ["212", "315", "332", "347", "363", "516", "518", "585", "607", "631", "646", "680", "716", "718", "838", "845", "914", "917", "929", "934"],
            "North Carolina": ["252", "336", "472", "704", "743", "828", "910", "919", "980", "984"],
            "North Dakota": ["701"],
            "Ohio": ["216", "220", "234", "326", "330", "380", "419", "440", "513", "567", "614", "740", "937"],
            "Oklahoma": ["405", "539", "572", "580", "918"],
            "Oregon": ["458", "503", "541", "971"],
            "Pennsylvania": ["215", "223", "267", "272", "412", "445", "484", "570", "582", "610", "717", "724", "814", "835", "878"],
            "Rhode Island": ["401"],
            "South Carolina": ["803", "839", "843", "854", "864"],
            "South Dakota": ["605"],
            "Tennessee": ["423", "615", "629", "731", "865", "901", "931"],
            "Texas": ["210", "214", "254", "281", "325", "346", "361", "409", "430", "432", "469", "512", "682", "713", "726", "737", "806", "817", "830", "832", "903", "915", "936", "940", "945", "956", "972", "979"],
            "Utah": ["385", "435", "801"],
            "Vermont": ["802"],
            "Virginia": ["276", "434", "540", "571", "703", "757", "804", "826", "948"],
            "Washington": ["206", "253", "360", "425", "509", "564"],
            "West Virginia": ["304", "681"],
            "Wisconsin": ["262", "414", "534", "608", "715", "920"],
            "Wyoming": ["307"],
        }
        self.addresses = {
            "Alabama": "123 Main St, Montgomery, AL",
            "Alaska": "456 Snow Rd, Juneau, AK",
            "Arizona": "789 Desert Blvd, Phoenix, AZ",
            "Arkansas": "101 River Ln, Little Rock, AR",
            "California": "102 Beach Ave, Los Angeles, CA",
            "Colorado": "103 Mountain Pass, Denver, CO",
            "Connecticut": "104 Maple St, Hartford, CT",
            "Delaware": "105 Bayshore Dr, Dover, DE",
            "Florida": "106 Sunshine Pkwy, Miami, FL",
            "Georgia": "107 Peachtree St, Atlanta, GA",
            "Hawaii": "108 Volcano St, Honolulu, HI",
            "Idaho": "109 Potato Rd, Boise, ID",
            "Illinois": "110 Windy Way, Chicago, IL",
            "Indiana": "111 Racecar Ave, Indianapolis, IN",
            "Iowa": "112 Cornfield Ln, Des Moines, IA",
            "Kansas": "113 Sunflower Rd, Topeka, KS",
            "Kentucky": "114 Bluegrass Blvd, Frankfort, KY",
            "Louisiana": "115 Bayou Ln, Baton Rouge, LA",
            "Maine": "116 Lobster Way, Augusta, ME",
            "Maryland": "117 Crab Cove, Annapolis, MD",
            "Massachusetts": "118 Tea Party Rd, Boston, MA",
            "Michigan": "119 Lake Shore Dr, Lansing, MI",
            "Minnesota": "120 Snowy Trail, St. Paul, MN",
            "Mississippi": "121 Delta Dr, Jackson, MS",
            "Missouri": "122 Arch St, Jefferson City, MO",
            "Montana": "123 Big Sky Rd, Helena, MT",
            "Nebraska": "124 Prairie Path, Lincoln, NE",
            "Nevada": "125 Casino Blvd, Carson City, NV",
            "New Hampshire": "126 Granite St, Concord, NH",
            "New Jersey": "127 Boardwalk, Trenton, NJ",
            "New Mexico": "128 Chili Pepper Ln, Santa Fe, NM",
            "New York": "129 Broadway, Albany, NY",
            "North Carolina": "130 Tobacco Rd, Raleigh, NC",
            "North Dakota": "131 Oil Dr, Bismarck, ND",
            "Ohio": "132 Buckeye St, Columbus, OH",
            "Oklahoma": "133 Twister Alley, Oklahoma City, OK",
            "Oregon": "134 Trail End, Salem, OR",
            "Pennsylvania": "135 Liberty Bell Blvd, Harrisburg, PA",
            "Rhode Island": "136 Ocean Ave, Providence, RI",
            "South Carolina": "137 Palmetto St, Columbia, SC",
            "South Dakota": "138 Rushmore Rd, Pierre, SD",
            "Tennessee": "139 Music Row, Nashville, TN",
            "Texas": "140 Lone Star Ln, Austin, TX",
            "Utah": "141 Salt Flats Rd, Salt Lake City, UT",
            "Vermont": "142 Maple Syrup Ln, Montpelier, VT",
            "Virginia": "143 History Ln, Richmond, VA",
            "Washington": "144 Raindrop Dr, Olympia, WA",
            "West Virginia": "145 Coal Rd, Charleston, WV",
            "Wisconsin": "146 Cheese Curd Ct, Madison, WI",
            "Wyoming": "147 Cowboy Rd, Cheyenne, WY"
        }
        

    @staticmethod
    def cargar_datos_desde_txt(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def generar_nombre_aleatorio(self):
        return random.choice(self.nombres)

    def generar_apellido_aleatorio(self):
        return random.choice(self.apellidos)

    def generar_alias_aleatorio(self):
        return random.sample(self.aliases, k=min(len(self.aliases), 3))

    def generar_fecha_nacimiento_aleatoria(self):
        start_date = pd.to_datetime("1900-01-01")
        end_date = pd.to_datetime("2003-01-01")
        dias_entre_fechas = (end_date - start_date).days
        dias_aleatorios = random.randrange(dias_entre_fechas)
        fecha_aleatoria = start_date + pd.Timedelta(days=dias_aleatorios)
        return fecha_aleatoria.strftime('%Y-%m-%d')

        # Asegúrate de que el archivo de nombres y otros recursos estén correctamente manejados.
    def introduce_typo(self, text):
        if len(text) > 1:
        # Intercambiar dos letras en una posición aleatoria.
            pos = random.randint(0, len(text) - 2)
            typo_text = text[:pos] + text[pos + 1] + text[pos] + text[pos + 2:]
            return typo_text
        return text
    
    def generate_phone(self, state):
        """Genera un número de teléfono basado en el estado proporcionado."""
        area_code = random.choice(self.area_codes.get(state, ["000"]))
        phone_number = f"{area_code}-{''.join(random.choices('0123456789', k=7))}"
        return phone_number

    def generate_address(self, state):
        """Devuelve una dirección basada en el estado proporcionado, escogida de manera pseudoaleatoria."""
        # Si el estado tiene direcciones definidas, elige una al azar.
        # Si no, devuelve una dirección genérica desconocida.
        return random.choice(self.addresses.get(state, ["123 Main St, Unknown State"]))
    


    def calculate_similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def generate_records(self):
        # Método principal para generar los registros según la configuración
        for seed_index, seed_row in self.seed_records.iterrows():
            seed_record = seed_row.to_dict()
            # Asegurar que la fecha de nacimiento cumpla la restricción de edad > 18 años
            self.validate_dob(seed_record)
            # Generar registros para cada tipo de caso configurado
            for arc in self.config['arcs']:
                self.generate_arc(seed_record, arc)
        


    def validate_and_adjust_dob(self, dob):
            """Ajusta la fecha de nacimiento para asegurar que sea de una persona mayor de 18 años."""
            dob_datetime = pd.to_datetime(dob)
            today = pd.to_datetime('today')
            if (today - dob_datetime).days / 365.25 < 18:
                dob_datetime = today - pd.DateOffset(years=18)
            return dob_datetime.strftime('%Y-%m-%d')



    def generate_similar_record(self, seed_record, sub_case=None):
            record = seed_record.copy()

            # Seleccionar nombres aleatorios para FirstName y LastName
            record['FirstName'] = random.choice(self.nombres)
            record['LastName'] = random.choice(self.nombres)

            # Generar dirección y teléfono basados en el estado
            state = record.get('Address-1 State', '')
            record['Address-1 Line 1'] = self.generate_address(state)
            record['Phone-1'] = self.generate_phone(state)

            # Añadir lógica para otros casos y subcasos si es necesario
            if sub_case == "TYPO":
                record['FirstName'] = self.introduce_typo(record['FirstName'])
                record['MatchScore'] = 0.9
                record['CaseType'] = "TYPO"
            else:
                record['MatchScore'] = 0.95
                record['CaseType'] = "SAME"

            # Asegurar que el DOB sea para mayores de 18 años
            record['Date of Birth'] = self.validate_and_adjust_dob(record['Date of Birth'])

            return record


    def format_record(self, record):
        # Incrementamos el ID actual y lo asignamos al registro
        if self.current_id is None:
            self.current_id = 1
        # # record['ID'] = self.current_id
        # self.current_id += 1  # Incrementamos el ID para el próximo registro

        formatted = (
            f"{record.get('ID', '')}|"
            f"{record.get('Prefix', '')}|"
            f"{record.get('FirstName', '')}|"
            f"{record.get('MiddleName', '')}|"
            f"{record.get('LastName', '')}|"
            f"{record.get('Suffix', '')}|"
            f"{record.get('Name Alias-1', '')},{record.get('Name Alias-2', '')},{record.get('Name Alias-3', '')}|"
            f"{record.get('DOB', '')}|"
            f"{record.get('SSN', '')}|"
            f"{record.get('Address-1 Line 1', '')}|"
            f"{record.get('Address-1 Line 2', '')}|"
            f"{record.get('Address-1 City', '')}|"
            f"{record.get('Address-1 State', '')}|"
            f"{record.get('Address-1 Zip', '')}|"
            f"{record.get('Address-1 Zip4', '')}|"
            f"{record.get('Address-2 Line 1', '')}|"
            f"{record.get('Address-2 Line 2', '')}|"
            f"{record.get('Address-2 City', '')}|"
            f"{record.get('Address-2 State', '')}|"
            f"{record.get('Address-2 Zip', '')}|"
            f"{record.get('Address-2 Zip4', '')}|"
            f"{record.get('Phone-1 Area Code', '')}-{record.get('Phone-1 Base Number', '')}|"
            f"{record.get('Phone-2 Area Code', '')}-{record.get('Phone-2 Base Number', '')}|"
            f"{record.get('Gender', '')}|"
            f"{record.get('MatchScore', '')}|"
            f"{record.get('CaseType', '')}"
        )
        return formatted



    def validate_seed_records(self):
        if 'Date of Birth' not in self.seed_records.columns:
            raise ValueError("La columna 'Date of Birth' es requerida.")

    def generate_records(self):
        # Asumiendo una estructura de configuración dada, generamos los registros.
        for arc in self.config['arcs']:
            # Generar registros por cada arco
            pass  # Implementación detallada

    # Ejemplo de generación de registro que cumple con las restricciones de edad
    def generate_record_with_age_restriction(self, seed_record):
        record = seed_record.copy()
        dob = datetime.strptime(record['Date of Birth'], '%Y-%m-%d')
        if (datetime.now() - dob).days / 365.25 < 18:
            raise ValueError("La persona debe ser mayor de 18 años.")
        return record

    # Cálculo simplificado de semejanza
    def calculate_similarity(self, record1, record2):
        # Implementar lógica de cálculo
        pass




    def generate_records(self):
        first_row = self.seed_records.iloc[0].to_dict()
        generated_records = []

        for case in self.config["cases"]:
            case_records_count = int(self.config["records_per_arc"] * case["distribution"])
            for sub_case in case.get("sub_cases", []):
                sub_case_records_count = int(case_records_count * sub_case["distribution"])
                for _ in range(sub_case_records_count):
                    if sub_case["case_id"] == "SAME" or sub_case["case_id"] == "TYPO":
                        record = self.generate_similar_record(first_row, sub_case["case_id"])
                    elif sub_case["case_id"] == "TWINS":
                        record = self.generate_twins_record(first_row)
                    elif sub_case["case_id"] == "PARENT_CHILD":
                        record = self.generate_parent_child_record(first_row)
                    elif sub_case["case_id"] == "SIBLINGS":
                        record = self.generate_siblings_record(first_row)
                    elif sub_case["case_id"] == "NOMATCH_FN_DOB":
                        record = self.generate_nomatch_fn_dob_record(first_row)
                    elif sub_case["case_id"] == "NOMATCH_LN_DOB":
                        record = self.generate_nomatch_ln_dob_record(first_row)
                    elif sub_case["case_id"] == "NOMATCH_SSN":
                        record = self.generate_nomatch_ssn_record(first_row)
                    elif sub_case["case_id"] == "NOMATCH_DOB_ZIP":
                        record = self.generate_nomatch_dob_zip_record(first_row)
                    else:
                        continue  # Omitir si el case_id no es reconocido

                    # Asegúrate de que format_record incluya todos los campos necesarios
                    formatted_record = self.format_record(record)
                    generated_records.append(formatted_record)
                    print(formatted_record)  # Imprime cada registro formateado en la consola

        return generated_records




    def generate_twins_record(self, seed_record):
        record = seed_record.copy()
        # Asegurar que el apellido sea el mismo
        record['CaseType'] = "TWINS"
        # Verificar que el apellido sea el mismo que el del registro original
        last_name = record.get('LastName', '')
        if last_name != '':
            # Generar un SSN con solo un dígito diferente en los últimos 4 dígitos
            ssn = list(str(record.get('SSN', '')))
            last_four_digits = ssn[-4:]
            # Elegir un dígito aleatorio para cambiar
            index_to_change = random.randint(0, 3)
            # Cambiar el dígito seleccionado
            new_digit = str((int(last_four_digits[index_to_change]) + random.randint(1, 9)) % 10)
            last_four_digits[index_to_change] = new_digit
            # Actualizar el SSN en el registro
            ssn[-4:] = last_four_digits
            record['SSN'] = ''.join(ssn)
            # Asegurar que el DOB sea el mismo que el del registro original
            record['DOB'] = seed_record.get('DOB', '')
            # Asegurar que al menos una de las direcciones sea la misma que la del registro original
            address_keys = ['Address-1 Line 1', 'Address-1 Line 2', 'Address-1 City', 'Address-1 State', 'Address-1 Zip', 'Address-1 Zip4']
            for key in address_keys:
                record[key] = seed_record.get(key, '')
            # Asegurar que el MatchScore sea adecuado para el caso TWINS
            record['MatchScore'] = 0.85  # Ejemplo de valor, ajusta según la necesidad
        return record

    def generate_parent_child_record(self, seed_record):
        record = seed_record.copy()
        # Asegurar que el apellido sea el mismo
        record['CaseType'] = "PARENT-CHILD"
        # Asegurar que el DOB esté separado por al menos 20 años
        dob = pd.to_datetime(record.get('Date of Birth'))
        record['Date of Birth'] = (dob - pd.DateOffset(years=20)).strftime('%Y-%m-%d')
        # Verificar si el sufijo es 'Jr' o 'Sr' y cambiarlo en consecuencia
        suffix = record.get('Suffix', '')
        if 'Jr' in suffix:
            record['Suffix'] = 'Sr'
        elif 'Sr' in suffix:
            record['Suffix'] = 'Jr'
        # Asegurar que al menos una de las direcciones sea la misma que la del registro original
        address_keys = ['Address-1 Line 1', 'Address-1 Line 2', 'Address-1 City', 'Address-1 State', 'Address-1 Zip', 'Address-1 Zip4']
        for key in address_keys:
            record[key] = seed_record.get(key, '')
        # Asegurar que el MatchScore sea adecuado para el caso PARENT-CHILD
        record['MatchScore'] = 0.92  # Ejemplo de valor, ajusta según la necesidad
        return record

    def generate_siblings_record(self, seed_record):
        record = seed_record.copy()
        # Asegurar que el apellido sea el mismo
        record['CaseType'] = "SIBLINGS"
        # Asegurar que el MatchScore sea adecuado para el caso SIBLINGS
        record['MatchScore'] = 0.88  # Ejemplo de valor, ajusta según la necesidad
        return record   


    def calculate_similarity(self, a, b):
        """Calcula la semejanza entre dos cadenas y retorna un valor entre 0 y 1."""
        return SequenceMatcher(None, a, b).ratio()

    def NOMATCH_FN_DOB(self, first_name1, first_name2, dob1, dob2):
        """Verifica la semejanza basada en el primer nombre y fecha de nacimiento."""
        if dob1 == dob2:
            similarity = self.calculate_similarity(first_name1, first_name2)
            if similarity >= 0.4:  # Asegura que la semejanza sea al menos del 40%
                return True
        return False

    def NOMATCH_LN_DOB(self, lastname1, lastname2, dob1, dob2):
        """Verifica la semejanza basada en el apellido y fecha de nacimiento."""
        if dob1 == dob2:
            similarity = self.calculate_similarity(lastname1, lastname2)
            if similarity >= 0.4:  # Corregido para comparar correctamente con 0.4 en lugar de 40
                return True
        return False

    def NOMATCH_SSN(self, ssn1, ssn2):
        """Verifica la semejanza basada en el número de seguro social."""
        similarity = self.calculate_similarity(ssn1, ssn2)
        if similarity >= 0.1:  # Corregido para usar 0.1 en la comparación, equivalente al 10%
            return True
        return False

    def NOMATCH_DOB_ZIP(self, dob1, dob2, zip1, zip2):
        """Verifica la semejanza basada en la fecha de nacimiento y el código postal."""
        similarity_dob = self.calculate_similarity(dob1, dob2)
        similarity_zip = self.calculate_similarity(zip1, zip2)
        if similarity_dob >= 0.1 and similarity_zip >= 0.1:  # Asegura que ambas semejanzas sean al menos del 10%
            return True
        return False
        

    def generate_nomatch_fn_dob_record(self, seed_record):
        record = seed_record.copy()
        if self.NOMATCH_FN_DOB(seed_record['FirstName'], seed_record['FirstName'], seed_record['Date of Birth'], seed_record['Date of Birth']):
            record['MatchScore'] = 0.4
            record['CaseType'] = 'NOMATCH_FN_DOB'  # Agrega esta línea
        else:
            record['MatchScore'] = 0
            record['CaseType'] = 'NOMATCH_FN_DOB'  # Agrega esta línea también para consistencia
        return record

    def generate_nomatch_ln_dob_record(self, seed_record):
        record = seed_record.copy()
        if self.NOMATCH_LN_DOB(seed_record['LastName'], "OtroApellido", seed_record['Date of Birth'], "OtraFechaDeNacimiento"):
            record['MatchScore'] = 0.4
            record['CaseType'] = 'NOMATCH_LN_DOB'  # Agrega esta línea
        else:
            record['MatchScore'] = 0
            record['CaseType'] = 'NOMATCH_LN_DOB'  # Y esta línea también
        return record

    


    def generate_nomatch_ssn_record(self, seed_record):
        record = seed_record.copy()
        original_ssn = str(seed_record['SSN'])
        if len(original_ssn) > 0:
            modified_ssn = original_ssn[:-1] + str((int(original_ssn[-1]) + 1) % 10)
        else:
            modified_ssn = "000000001"
        record['SSN'] = modified_ssn
        record['MatchScore'] = 0.1
        record['CaseType'] = 'NOMATCH_SSN'  # Agrega esta línea
        return record

        


    
        

    def generate_nomatch_dob_zip_record(self, seed_record):
        record = seed_record.copy()
        original_dob = pd.to_datetime(seed_record['Date of Birth'])
        modified_dob = original_dob + pd.DateOffset(years=1)
        record['Date of Birth'] = modified_dob.strftime('%Y-%m-%d')
        original_zip = str(seed_record['Address-1 Zip'])
        modified_zip = str(int(original_zip) + 1).zfill(5)
        record['Address-1 Zip'] = modified_zip
        record['MatchScore'] = 0.1
        record['CaseType'] = 'NOMATCH_DOB_ZIP'  # Agrega esta línea
        return record



