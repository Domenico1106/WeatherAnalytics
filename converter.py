# Author: Giuseppe Cavallo
# Date: 05/09/2023

import os
import csv
from tqdm import tqdm

cartelle = ['QCLCD201301','QCLCD201302','QCLCD201303','QCLCD201304','QCLCD201305','QCLCD201306','QCLCD201307','QCLCD201308','QCLCD201309','QCLCD201310','QCLCD201311','QCLCD201312']
mese = 1

massimo_numero_di_righe = 1048576  # Imposta il numero massimo di righe per ciascun file CSV

for cartella in cartelle:
    cartella_destinazione = f"CSV20130{mese}"
    mese += 1

    if not os.path.exists(cartella_destinazione):
        os.makedirs(cartella_destinazione)

    for nome_file in os.listdir(cartella):
        if nome_file.endswith(".txt"):
            input_file_path = os.path.join(cartella, nome_file)

            # Calcola il numero di righe nel file di testo
            linee = sum(1 for linea in open(input_file_path))

            if linee <= massimo_numero_di_righe:
                # Se il file ha meno o uguale al numero massimo di righe per file, elabora normalmente
                output_file_path = os.path.join(cartella_destinazione, nome_file.replace(".txt", ".csv"))

                with open(input_file_path, "r") as txt_file, open(output_file_path, "w", newline="") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    # il successivo frammento crea una barra di avanzamento per tenere conto della conversione durante l'esecuzione del programma
                    with tqdm(total=linee, unit="line") as pbar:
                        for linea in txt_file:
                            csv_writer.writerow(linea.strip().split(","))
                            pbar.update(1)
            else:
                # Se il file ha più righe del limite, suddividilo in più file CSV
                base_output_filename = nome_file.replace(".txt", "_part")
                part_num = 1
                righe_scritte = 0

                with open(input_file_path, "r") as txt_file:
                    while righe_scritte < linee:
                        output_file_path = os.path.join(cartella_destinazione, f"{base_output_filename}_{part_num}.csv")

                        with open(output_file_path, "w", newline="") as csv_file:
                            csv_writer = csv.writer(csv_file)
                            rows_in_this_part = min(massimo_numero_di_righe, linee - righe_scritte)
                         # il successivo frammento crea una barra di avanzamento per tenere conto della conversione durante l'esecuzione del programma
                            with tqdm(total=rows_in_this_part, unit="line") as pbar:
                                for _ in range(rows_in_this_part):
                                    linea = txt_file.readline()
                                    if not linea:
                                        break  # Fine del file di input
                                    csv_writer.writerow(linea.strip().split(","))
                                    righe_scritte += 1
                                    pbar.update(1)
                        part_num += 1

