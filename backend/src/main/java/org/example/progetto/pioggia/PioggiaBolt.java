package org.example.progetto.pioggia;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;
import org.example.progetto.utils.Utilities;

import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.*;

@SuppressWarnings("ALL")
public class PioggiaBolt extends BaseRichBolt {

    private OutputCollector outputCollector;
    private final Map<String, Double> pioggia_mensile = new HashMap<>(), mese_pioggia = new HashMap<>(),
            pioggia_annuale = new HashMap<>(), pioggia_giornaliera = new HashMap<>();

    private void analisiMensile(Map<String, Double> mappa) {
        for (int i = 0; i < Utilities.MESI.length; i++) {

            int giorni_mese = Utilities.contaGiorni(new DecimalFormat("00").format(i + 1));
            Map<String, Double> media_pioggia_citta_mese = new HashMap<>();
            for (String chiave : Utilities.capitali.keySet()) {
                double pioggia_totale = mappa.get(String.format("%02d_%s", i + 1, chiave)) * 25.4;
                Utilities.aggiornaMappa(mese_pioggia, Utilities.MESI[i], pioggia_totale);
                media_pioggia_citta_mese.put(chiave, pioggia_totale / giorni_mese);
            }//for

            try {
                FileWriter fileWriter = new FileWriter(String.format("risultati_piogge/2013_%s_Pioggia.csv", Utilities.MESI[i]));
                fileWriter.write("wban_mensile; country_state; rain; rainiest_day; rainiest_month; rainiest_country_state; rainiest_value; less_rainy_day; less_rainy_month; less_rainy_country_state; less_rainy_value\n");
                int j = 0;
                for (Map.Entry<String, Double> elemento : media_pioggia_citta_mese.entrySet()) {
                    if (j == 0) {
                        fileWriter.write(String.format("%s; %s; %s; ", elemento.getKey(), Utilities.capitali.get(elemento.getKey()), (new DecimalFormat("0.00").format(elemento.getValue())).replace(",",".")));
                        analisiGiornaliera(i, fileWriter);

                    }//if
                    else
                        fileWriter.write(String.format("%s; %s; %s\n", elemento.getKey(), Utilities.capitali.get(elemento.getKey()), (new DecimalFormat("0.00").format(elemento.getValue())).replace(",",".")));
                    j++;
                }//for
                fileWriter.close();
            } catch (IOException e) {
                e.printStackTrace();
            }//catch
        }//for
    }//analisiMensile

    private void analisiAnnuale(Map<String, Double> mappa) {
        try {
            FileWriter fileWriter = new FileWriter("risultati_piogge/2013_Pioggia.csv");
            fileWriter.write("mese; pioggia\n");
            for(String mese : Utilities.MESI)

                fileWriter.write(String.format("%s; %s\n", mese,

                        (new DecimalFormat("0.00").format((mappa.get(mese) / Utilities.contaGiorni(mese)) / Utilities.capitali.size())).replace(',','.')));
            fileWriter.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }//catch
    }//analisiAnnuale

    private void analisiGiornaliera(int mese, FileWriter fileWriter) throws IOException {
        String giorno_massimo = "", giorno_minimo = "";
        double pioggia_massima = Double.MIN_VALUE, pioggia_minima = Double.MAX_VALUE;

        for (String chiave : pioggia_giornaliera.keySet())
            if (new DecimalFormat("00").format(mese + 1).equals(chiave.substring(0, 2))) {
                if (pioggia_giornaliera.get(chiave) > pioggia_massima) {
                    pioggia_massima = pioggia_giornaliera.get(chiave);
                    giorno_massimo = chiave; //0101_03084
                }//if

                /** nella successiva analisi consideriamo solo valori maggiori di una pioggia debole (1.5 mm == 0.06 inch)*/
                if (pioggia_giornaliera.get(chiave) < pioggia_minima && pioggia_giornaliera.get(chiave) > 0.06) {
                    pioggia_minima = pioggia_giornaliera.get(chiave);
                    giorno_minimo = chiave; //0101_03084
                }//if
            }//if esterno

        fileWriter.write(String.format("%s; %s; %s; %s; ", giorno_massimo.substring(2, 4), Utilities.MESI[Integer.valueOf(giorno_massimo.substring(0, 2)) - 1],
                Utilities.capitali.get(giorno_massimo.substring(5)),
                (new DecimalFormat("0.00").format(pioggia_massima * 25.4)).replace(',','.')));

        fileWriter.write(String.format("%s; %s; %s; %s\n", giorno_minimo.substring(2, 4), Utilities.MESI[Integer.valueOf(giorno_minimo.substring(0, 2)) - 1],
                Utilities.capitali.get(giorno_minimo.substring(5)),
                (new DecimalFormat("0.00").format(pioggia_minima * 25.4)).replace(',','.')));
    }//analisiGiornaliera

    public void emettiTuple() {
        outputCollector.emit(new Values(pioggia_mensile, pioggia_annuale, pioggia_giornaliera));
    }//emettiTuple

    @Override
    public void prepare(Map<String, Object> map, TopologyContext topologyContext, OutputCollector outputCollector) {
        this.outputCollector = outputCollector;
    }//prepare

    @Override
    public void execute(Tuple tuple) {
        String wban_citta = tuple.getStringByField("wban");
        String pioggia = tuple.getStringByField("pioggia");
        String mese_giorno = tuple.getStringByField("mese_giorno");
        String mese = mese_giorno.substring(0, 2);

        String chiave = mese + "_" + wban_citta;
        String chiave_giornaliera = mese_giorno + "_" + wban_citta;

        double qta_pioggia;
        if (pioggia.contains("T"))
            qta_pioggia = 0.005;
        else if (pioggia.contains("."))
            qta_pioggia = Double.parseDouble(pioggia);
        else qta_pioggia = 0.0;

        Utilities.aggiornaMappa(pioggia_mensile, chiave, qta_pioggia);
        Utilities.aggiornaMappa(pioggia_annuale, wban_citta, qta_pioggia);
        if (qta_pioggia != 0)
            Utilities.aggiornaMappa(pioggia_giornaliera, chiave_giornaliera, qta_pioggia);
        emettiTuple();
    }//execute

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
        outputFieldsDeclarer.declare(new Fields("pioggia_mesi", "pioggia_anno", "pioggia_giornaliera"));
    }//declareOutputFields

    @Override
    public void cleanup() {
        analisiMensile(pioggia_mensile);
        analisiAnnuale(mese_pioggia);
    }//cleanup
}//class PioggiaBolt
