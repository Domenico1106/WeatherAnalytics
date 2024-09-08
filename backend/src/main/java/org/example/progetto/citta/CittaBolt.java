package org.example.progetto.citta;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;
import org.example.progetto.utils.Utilities;

import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.*;

@SuppressWarnings("ALL")
public class CittaBolt extends BaseRichBolt {
    private HashMap<String, List<Double>> temperature_massime = new HashMap<>();
    private HashMap<String, List<Double>> temperature_minime = new HashMap<>();
    private HashMap<String, List<Double>> temperature_medie = new HashMap<>();
    private final HashMap<String, Double> medie_medie = new HashMap<>();
    private HashMap<String, Double> pioggia_mensile = new HashMap<>();
    private HashMap<String, Double> pioggia_annuale = new HashMap<>(), pioggia_giornaliera = new HashMap<>();


    private List<Map.Entry<String, Double>> analisiAnnualeTemperatura(Map<String, List<Double>> mappa, FileWriter fileWriter) throws IOException {
        for (int mese = 0; mese < Utilities.MESI.length; mese++)
            for (String chiave : mappa.keySet())
                if (chiave.substring(0, 2).equals(new DecimalFormat("00").format(mese + 1))) {
                    double somma = 0.0;
                    for (Double temperatura : mappa.get(chiave))
                        somma += temperatura;

                    medie_medie.put(chiave, somma / mappa.get(chiave).size());
                }//if

        Map<String, List<Double>> citta_avgTempS = new HashMap<>();
        Map<String, Double> citta_avgTemp = new HashMap<>();

        for (String chiave : medie_medie.keySet())
            Utilities.aggiornaMappa(citta_avgTempS, chiave.substring(3), String.valueOf((medie_medie.get(chiave) * 1.8) + 32));

        for (String chiave : citta_avgTempS.keySet()) {
            double mediaAnnuale = 0.0;
            for (Double avg : citta_avgTempS.get(chiave))
                mediaAnnuale += avg;

            citta_avgTemp.put(chiave, mediaAnnuale / citta_avgTempS.get(chiave).size());
        }//for

        List<Map.Entry<String, Double>> lista = new LinkedList<>(citta_avgTemp.entrySet());
        lista.sort(Map.Entry.comparingByValue(Comparator.reverseOrder()));

        return lista;
    }//analisiAnnualeTemperatura

    private List<Map.Entry<String, Double>> analisiAnnualePioggia(Map<String, Double> mappa, FileWriter fileWriter) throws IOException {
        List<Map.Entry<String, Double>> ordered_value = new LinkedList<>(mappa.entrySet());
        ordered_value.sort(Map.Entry.comparingByValue(Comparator.reverseOrder()));
        return ordered_value;
    }//analisiAnnualePioggia

    private void calcoloPioggiaMaxMin(String wban, ArrayList<String> dati) {
        String mese_max = "", giorno_max = "";
        double pioggia_max = Double.MIN_VALUE;
        String mese_min = "", giorno_min = "";
        double pioggia_min = Double.MAX_VALUE;

        for (String chiave : pioggia_giornaliera.keySet()) {//0101_
            if (chiave.substring(5).equals(wban)) {
                if (pioggia_giornaliera.get(chiave) * 25.4 > pioggia_max) {
                    pioggia_max = pioggia_giornaliera.get(chiave) * 25.4;
                    mese_max = chiave.substring(0, 2);
                    giorno_max = chiave.substring(2, 4);
                }//if

                if (pioggia_giornaliera.get(chiave) * 25.4 < pioggia_min && pioggia_giornaliera.get(chiave) * 25.4 > 1.5) {
                    pioggia_min = pioggia_giornaliera.get(chiave) * 25.4;
                    mese_min = chiave.substring(0, 2);
                    giorno_min = chiave.substring(2, 4);
                }//if
            }//if esterno
        }//for
        dati.add(mese_max);
        dati.add(giorno_max);
        dati.add(new DecimalFormat("0.00").format(pioggia_max));
        dati.add(mese_min);
        dati.add(giorno_min);
        dati.add(new DecimalFormat("0.00").format(pioggia_min));

    }//calcoloPioggiaMaxMin

    private void calcoloTempMaxMin(String wban, ArrayList<String> dati) {
        String mese_max = "", mese_min = "";
        HashMap<String, Double> meseMax = new HashMap<>(), meseMin = new HashMap<>();
        double max = Double.MIN_VALUE, min = Double.MAX_VALUE;

        for (String chiave : temperature_massime.keySet())
            if (chiave.substring(3).equals(wban))
                meseMax.put(chiave.substring(0, 2), temperature_massime.get(chiave).stream().max(Double::compare).orElse(Double.NaN));

        for (String mese : meseMax.keySet())
            if (meseMax.get(mese) > max) {
                max = meseMax.get(mese);
                mese_max = Utilities.MESI[Integer.parseInt(mese) - 1];
            }//if

        for (String chiave : temperature_minime.keySet())
            if (chiave.substring(3).equals(wban))
                meseMin.put(chiave.substring(0, 2), temperature_minime.get(chiave).stream().min(Double::compare).orElse(Double.NaN));

        for (String mese : meseMin.keySet())
            if (min > meseMin.get(mese)) {
                min = meseMin.get(mese);
                mese_min = Utilities.MESI[Integer.parseInt(mese) - 1];
            }//if
        dati.add(mese_max);
        dati.add(new DecimalFormat("0.00").format(max));

        dati.add(mese_min);
        dati.add(new DecimalFormat("0.00").format(min));

    }//calcoloAvgTempMaxMin

    private List<String> monthlyAvgPioggia(String wban, ArrayList<String> dati) {
        ArrayList<String> risultato = new ArrayList<>();

        for (int mese = 0; mese < Utilities.MESI.length; mese++) {
            double pioggia_media;
            int giorni_mese = Utilities.contaGiorni(new DecimalFormat("00").format(mese));
            pioggia_media = (pioggia_mensile.get(new DecimalFormat("00").format(mese + 1) + "_" + wban) * 25.4) / giorni_mese;
            risultato.add(String.format("%s:%s", Utilities.MESI[mese], new DecimalFormat("0.00").format(pioggia_media)));
        }//for
        return risultato;
    }//monthlyAvgPioggia

    private List<String> calcoloAvgTemp(String wban, ArrayList<String> dati) {
        ArrayList<String> risultato = new ArrayList<>();

        for (int i = 0; i < Utilities.MESI.length; i++) {
            double avg = 0.0;
            for (Double temp : temperature_medie.get(new DecimalFormat("00").format(i + 1) + "_" + wban))
                avg += temp;

            avg = avg / temperature_medie.get(new DecimalFormat("00").format(i + 1) + "_" + wban).size();
            risultato.add(String.format("%s:%s", Utilities.MESI[i], new DecimalFormat("0.00").format(avg)));
        }//for
        return risultato;
    }//calcoloAvgTemp

    @Override
    public void prepare(Map<String, Object> map, TopologyContext topologyContext, OutputCollector outputCollector) {
    }//prepare

    @Override
    public void execute(Tuple tuple) {
        if (tuple.getSourceComponent().equals("pioggia_bolt")) {
            pioggia_mensile = (HashMap<String, Double>) tuple.getValueByField("pioggia_mesi");
            pioggia_annuale = (HashMap<String, Double>) tuple.getValueByField("pioggia_anno");
            pioggia_giornaliera = (HashMap<String, Double>) tuple.getValueByField("pioggia_giornaliera");
        } else if (tuple.getSourceComponent().equals("temperatura_bolt")) {
            temperature_massime = (HashMap<String, List<Double>>) tuple.getValueByField("temperature_massime");
            temperature_minime = (HashMap<String, List<Double>>) tuple.getValueByField("temperature_minime");
            temperature_medie = (HashMap<String, List<Double>>) tuple.getValueByField("temperature_medie");
        }//else if
    }//execute

    public void scriviFileAnnuale(List<Map.Entry<String, Double>> pioggia_anno, List<Map.Entry<String, Double>> temperatura_anno, FileWriter fileWriter) throws IOException {
        ListIterator<Map.Entry<String, Double>> it_piogge = pioggia_anno.listIterator();
        ListIterator<Map.Entry<String, Double>> it_temperature = temperatura_anno.listIterator();

        while (it_piogge.hasNext()) { /**non serve inserire nella condizione anche it_temperature.hasNext() in quanto le liste
                                            cui fanno riferimento gli iteratori hanno la stessa size */

            Map.Entry<String, Double> curr_pioggia = it_piogge.next();
            Map.Entry<String, Double> curr_temperatura = it_temperature.next();

            String citta_pioggia = Utilities.capitali.get(curr_pioggia.getKey());
            String citta_temperatura = Utilities.capitali.get(curr_temperatura.getKey());

            fileWriter.write(String.format("%s; %s; %s; %s\n",
                    citta_pioggia,
                    (new DecimalFormat("0.00").format((curr_pioggia.getValue() * 25.4) / 365)).replace(',', '.'),
                    citta_temperatura,
                    (new DecimalFormat("0.00").format(curr_temperatura.getValue())).replace(',', '.')
            ));
        }//while
    }//scriviFileAnnuale

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
    }//declareOutputFields

    @Override
    public void cleanup() {
        try {
            FileWriter fileWriter0 = new FileWriter("risultati_citta/2013_Citta.csv");
            fileWriter0.write("rain_country_state; rain; temp_country_state; temp\n");

            List<Map.Entry<String, Double>> pioggia_anno = analisiAnnualePioggia(pioggia_annuale, fileWriter0);
            List<Map.Entry<String, Double>> temperatura_anno = analisiAnnualeTemperatura(temperature_medie, fileWriter0);

            scriviFileAnnuale(pioggia_anno, temperatura_anno, fileWriter0);

            fileWriter0.close();

            for (String wban : Utilities.capitali.keySet()) {
                ArrayList<String> dati = new ArrayList<>();

                /*** Struttura della lista dati:
                 *  0               1          2       3               4          5         6           7       8             9
                 * [mesePioggiaMax, giornoMax, qtaMax, mesePioggiaMin, giornoMin, qtaMin, meseTempMax, tempMax, meseTempMin, tempMin]
                 ***/

                calcoloPioggiaMaxMin(wban, dati);
                calcoloTempMaxMin(wban, dati);
                List<String> mediaPiogge = monthlyAvgPioggia(wban, dati);
                List<String> mediaTemperature = calcoloAvgTemp(wban, dati);

                FileWriter fileWriter = new FileWriter(String.format("risultati_citta/2013_%s.csv", Utilities.capitali.get(wban)));

                fileWriter.write("rainest_day; rainest_month; max_rain; less_rainy_day; less_rainy_month; min_rain; hotter_month; max_temp; colder_month; min_temp; month_rain; monthly_rain_value; month_temp; monthly_temp_value\n");
                fileWriter.write(String.format("%s; %s; %s; %s; %s; %s; %s; %s; %s; %s; ", dati.get(1), Utilities.MESI[Integer.valueOf(dati.get(0)) - 1], dati.get(2).replace(',', '.'),
                        dati.get(4), Utilities.MESI[Integer.valueOf(dati.get(3)) - 1], dati.get(5).replace(',', '.'),
                        dati.get(6), dati.get(7).replace(',', '.'), dati.get(8), dati.get(9).replace(',', '.')));

                for (int i = 0; i < Utilities.MESI.length; i++)
                    if (i == 0)
                        fileWriter.write(String.format("%s; %s; %s; %s\n", mediaPiogge.get(i).split(":")[0],
                                mediaPiogge.get(i).split(":")[1].replace(',', '.'), mediaTemperature.get(i).split(":")[0],
                                mediaTemperature.get(i).split(":")[1].replace(',', '.')));
                    else
                        fileWriter.write(String.format("-; -; -; -; -; -; -; -; -; -; %s; %s; %s; %s\n", mediaPiogge.get(i).split(":")[0],
                                mediaPiogge.get(i).split(":")[1].replace(',', '.'), mediaTemperature.get(i).split(":")[0],
                                mediaTemperature.get(i).split(":")[1].replace(',', '.')));

                fileWriter.close();
            }//for
        } catch (IOException e) {
            throw new RuntimeException(e);
        }//catch
    }//cleanup
}//class CittaBolt
