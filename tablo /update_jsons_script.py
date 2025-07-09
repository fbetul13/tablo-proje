
import re

# backup.sql dosyasını satır satır oku
with open('backup.sql', 'r', encoding='utf-8') as f:
    lines = f.readlines()

update_sqls = []

# Tüm INSERT satırlarını tara
for line in lines:
    line_strip = line.strip()
    # logs tablosu
    match = re.match(r"INSERT INTO llm_platform.logs VALUES \((.*)\);", line_strip)
    if match:
        values_str = match.group(1)
        value_pattern = re.compile(r"'(?:[^']|''|\\\\')*'|NULL|\{.*?\}|[^,]+")
        values = [v.strip() for v in value_pattern.findall(values_str)]
        if len(values) >= 7:
            log_id = values[0]
            json_field = values[6]
            if json_field.startswith("'") and json_field.endswith("'"):
                json_data = json_field[1:-1].replace("''", "'")
            else:
                json_data = json_field
            json_data_sql = json_data.replace("'", "''")
            sql = f"UPDATE llm_platform.logs SET details = '{json_data_sql}' WHERE log_id = {log_id} AND (details IS NULL OR details = '' OR details = '{{}}');"
            update_sqls.append(sql)
        continue
    # Users tablosu
    match = re.match(r"INSERT INTO llm_platform.\"Users\" VALUES \((.*)\);", line_strip)
    if match:
        values_str = match.group(1)
        value_pattern = re.compile(r"'(?:[^']|''|\\')*'|NULL|\{.*?\}|[^,]+")
        values = [v.strip() for v in value_pattern.findall(values_str)]
        if len(values) >= 7:
            user_id = values[0]
            json_field = values[6]
            if json_field.startswith("'") and json_field.endswith("'"):
                json_data = json_field[1:-1].replace("''", "'")
            else:
                json_data = json_field
            json_data_sql = json_data.replace("'", "''")
            sql = f"UPDATE llm_platform.\"Users\" SET details = '{json_data_sql}' WHERE id = {user_id} AND (details IS NULL OR details = '' OR details = '{{}}');"
            update_sqls.append(sql)
        continue
    # assistants tablosu
    match = re.match(r"INSERT INTO llm_platform.assistants VALUES \((.*)\);", line_strip)
    if match:
        values_str = match.group(1)
        value_pattern = re.compile(r"'(?:[^']|''|\\')*'|NULL|\{.*?\}|[^,]+")
        values = [v.strip() for v in value_pattern.findall(values_str)]
        if len(values) >= 4:
            asistan_id = values[0]
            json_field = values[3]
            if json_field.startswith("'") and json_field.endswith("'"):
                json_data = json_field[1:-1].replace("''", "'")
            else:
                json_data = json_field
            json_data_sql = json_data.replace("'", "''")
            sql = f"UPDATE llm_platform.assistants SET details = '{json_data_sql}' WHERE asistan_id = {asistan_id} AND (details IS NULL OR details = '' OR details = '{{}}');"
            update_sqls.append(sql)
        continue
    # Diğer tüm tablolar (details, json, data, extra gibi json içeren alanlar olabilir)
    match = re.match(r"INSERT INTO llm_platform\.([a-zA-Z0-9_\"]+) VALUES \((.*)\);", line_strip)
    if match:
        table = match.group(1)
        values_str = match.group(2)
        value_pattern = re.compile(r"'(?:[^']|''|\\')*'|NULL|\{.*?\}|[^,]+")
        values = [v.strip() for v in value_pattern.findall(values_str)]
        # details, json, data, extra gibi json olabilecek alanları bul
        for idx, val in enumerate(values):
            if idx == 0:
                row_id = val
            # Alan adı bilinmiyorsa, sadece json gibi görünenleri güncelle
            if val.startswith("'{") and val.endswith("}'"):
                json_data = val[1:-1].replace("''", "'")
                json_data_sql = json_data.replace("'", "''")
                # Alan adını tahmin etmek için
                col_name = f'col{idx+1}'
                sql = f"-- Tahmini alan: {col_name}\n-- Tablo: {table}\n-- DİKKAT: Alan adı elle kontrol edilmeli!\n-- UPDATE llm_platform.{table} SET {col_name} = '{json_data_sql}' WHERE id = {row_id} AND ({col_name} IS NULL OR {col_name} = '' OR {col_name} = '{{}}');"
                update_sqls.append(sql)

# Sonuçları dosyaya yaz
with open('update_jsons.sql', 'w', encoding='utf-8') as f:
    for sql in update_sqls:
        f.write(sql + '\n')

print(f"{len(update_sqls)} adet UPDATE komutu üretildi. update_jsons.sql dosyasına kaydedildi.")
