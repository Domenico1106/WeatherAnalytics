package org.example.progetto.temperatura;

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
public class TemperaturaBolt extends BaseRichBolt {

    private final Map<String, List<Double>> temperature_massime = new HashMap<>(),
            temperature_medie = new HashMap<>(), temperature_minime = new HashMap<>();
    private final Map<String, Double> medie_medie = new HashMap<>(), escursione_annuale = new HashMap<>();
    private Map<String, Double> massime_medie = new HashMap<>(), minime_medie = new HashMap<>();

    private OutputCollector outputCollector;

    public void scriviTemperatureMedie(FileWriter fileWriter, int mese) throws IOException{

        int giorni = Utilities.contaGiorni(String.format("%02d", mese + 1));
        for(int i = 0; i < giorni; i++){
            double [] medie = {0.0, 0.0, 0.0};
            for(String wban : Utilities.capitali.keySet()){
                if(i < temperature_massime.get(String.format("%02d", mese + 1)+"_"+wban).size()){
                    medie[0] += temperature_massime.get(String.format("%02d", mese + 1)+"_"+wban).get(i);
                }
                if(i < temperature_minime.get(String.format("%02d", mese + 1)+"_"+wban).size()){
                    medie[1] += temperature_minime.get(String.format("%02d", mese + 1)+"_"+wban).get(i);
                }
                if(i < temperature_medie.get(String.format("%02d", mese + 1)+"_"+wban).size()){
                    medie[2] += temperature_medie.get(String.format("%02d", mese + 1)+"_"+wban).get(i);
                }
            }
            fileWriter.write(String.format("%02d; %.2f; %.2f; %.2f\n",i+1,medie[0]/49,medie[1]/49,medie[2]/49).replace(",", "."));
        }

    }//scriviTemperatureMedie

    public void sommaTemperatura(Map<String, List<Double>> mappa_massime, Map<String, List<Double>> mappa_minime, Map<String, List<Double>> mappa_medie, int mese, FileWriter fileWriter)throws IOException{
        double [] somme = {0.0, 0.0, 0.0};
        for(String chiave : mappa_massime.keySet()) {
            if (chiave.substring(0, 2).equals(String.format("%02d", mese + 1))) {
                somme[0] += mappa_massime.get(chiave).stream().mapToDouble(Double::doubleValue).sum() / (mappa_massime.get(chiave).size());
                somme[1] += mappa_minime.get(chiave).stream().mapToDouble(Double::doubleValue).sum() / (mappa_minime.get(chiave).size());
                somme[2] += mappa_medie.get(chiave).stream().mapToDouble(Double::doubleValue).sum() / (mappa_medie.get(chiave).size());
            }
        }
        fileWriter.write(String.format("%s; %.2f; %.2f; %.2f\n", Utilities.MESI[mese], somme[0]/49, somme[1]/49, somme[2]/49).replace(",","."));
    }//sommaTemperatura

    private void analisiMensile(Map<String, List<Double>> mappa, int mese, String tipo_analisi, FileWriter fileWriter) throws IOException {
        Map<String, Double> avg_temp = new HashMap<>();
        for (String chiave : mappa.keySet())
            if (chiave.substring(0, 2).equals(new DecimalFormat("00").format(mese + 1))) {
                double somma = 0.0;
                for (Double temperatura : mappa.get(chiave))
                    somma += temperatura;
                avg_temp.put(chiave, somma / mappa.get(chiave).size());
                if (tipo_analisi.equals("media")) {
                    medie_medie.put(chiave, somma / mappa.get(chiave).size());
                }
            }//if

        if (tipo_analisi.equals("massima"))
            massime_medie = avg_temp;
        else if (tipo_analisi.equals("minima"))
            minime_medie = avg_temp;

        LinkedList<Map.Entry<String, Double>> ordered_avg_temp = new LinkedList<>(avg_temp.entrySet());
        ordered_avg_temp.sort(Map.Entry.comparingByValue(Comparator.reverseOrder()));
        //fileWriter.write("avg_max_country, avg_max_state, avg_max_temp, avg_min_country, avg_min_state, avg_min_temp, max_max_country, max_max_state, max_max_temp, max_min_country, max_min_state, max_min_temp, min_max_country, min_max_state, min_max_temp, min_min_country, min_min_state, min_min_temp, avg_exc_temp, max_exc_temp, min_exc_temp");
        String  citta_stato_max = Utilities.capitali.get(ordered_avg_temp.getFirst().getKey().substring(3)),
                //stato_max = Utilities.capitali.get(ordered_avg_temp.getFirst().getKey().substring(3)).split(", ")[1],
                citta_stato_min = Utilities.capitali.get(ordered_avg_temp.getLast().getKey().substring(3));
                //stato_min = Utilities.capitali.get(ordered_avg_temp.getLast().getKey().substring(3)).split(", ")[1];
        fileWriter.write(String.format("%s; %s; %s; %s; ", citta_stato_max, (new DecimalFormat("0.00").format(ordered_avg_temp.getFirst().getValue())).replace(',','.'),
                citta_stato_min, (new DecimalFormat("0.00").format(ordered_avg_temp.getLast().getValue())).replace(',','.')));
    }//analisiMensile

    private void calcolaEscursioneTermicaMensile(Map<String, Double> massimeMedie, Map<String, Double> minimeMedie, int mese, FileWriter fileWriter) throws IOException {
        double escursioneMax;
        double escursioneMin;
        double escursioneAvg = 0.0;
        ArrayList<Double> valoriEscursione = new ArrayList<>();

        for (String chiave : massimeMedie.keySet())
            if (chiave.substring(0, 2).equals(new DecimalFormat("00").format(mese + 1))) {
                valoriEscursione.add(massimeMedie.get(chiave) - minimeMedie.get(chiave));
                escursioneAvg += massimeMedie.get(chiave) - minimeMedie.get(chiave);
            }//if

        escursioneMax = valoriEscursione.stream().max(Double::compare).orElse(Double.NaN);
        escursioneMin = valoriEscursione.stream().min(Double::compare).orElse(Double.NaN);
        escursioneAvg = escursioneAvg / valoriEscursione.size();

        escursione_annuale.put(new DecimalFormat("00").format(mese + 1) + "_max", escursioneMax);
        escursione_annuale.put(new DecimalFormat("00").format(mese + 1) + "_min", escursioneMin);
        escursione_annuale.put(new DecimalFormat("00").format(mese + 1) + "_avg", escursioneAvg);
        fileWriter.write(String.format("%s; %s; %s",(new DecimalFormat("0.00").format(escursioneAvg)).replace(',','.'), (new DecimalFormat("0.00").format(escursioneMax)).replace(',','.'),
                (new DecimalFormat("0.00").format(escursioneMin)).replace(',','.')));
    }//calcolaEscursioneTermicaMensile

    public void calcolaEscursioneTermicaAnnuale(Map<String, Double> mappa, FileWriter fileWriter) throws IOException {
        LinkedList<Double> max_min = new LinkedList<>(), avg = new LinkedList<>();
        String mese;

        for (String chiave : mappa.keySet())
            if (chiave.substring(3).equals("max") || chiave.substring(3).equals("min"))
                max_min.add(mappa.get(chiave));
            else
                avg.add(mappa.get(chiave));

        double escursione_massima = max_min.stream().max(Double::compare).orElse(Double.NaN),
                escursione_minima = max_min.stream().min(Double::compare).orElse(Double.NaN),
                escursione_media_massima = avg.stream().max(Double::compare).orElse(Double.NaN),
                escursione_media_minima = avg.stream().min(Double::compare).orElse(Double.NaN);

        for (Map.Entry<String, Double> record : mappa.entrySet())
            if (record.getValue() == escursione_massima) {
                mese = Utilities.MESI[Integer.parseInt(record.getKey().substring(0, 2)) - 1];
                fileWriter.write(String.format("%s; %s", mese, (new DecimalFormat("0.00").format(escursione_massima)).replace(',','.')));
            } else if (record.getValue() == escursione_minima) {
                mese = Utilities.MESI[Integer.parseInt(record.getKey().substring(0, 2)) - 1];
                fileWriter.write(String.format("%s; %s; ", mese, (new DecimalFormat("0.00").format(escursione_minima)).replace(',','.')));
            } else if (record.getValue() == escursione_media_massima) {
                mese = Utilities.MESI[Integer.parseInt(record.getKey().substring(0, 2)) - 1];
                fileWriter.write(String.format("%s; %s; ", mese, (new DecimalFormat("0.00").format(escursione_media_massima)).replace(',','.')));
            } else if (record.getValue() == escursione_media_minima) {
                mese = Utilities.MESI[Integer.parseInt(record.getKey().substring(0, 2)) - 1];
                fileWriter.write(String.format("%s; %s; ", mese, (new DecimalFormat("0.00").format(escursione_media_minima)).replace(',','.')));
            }//else if
    }//calcolaEscursioneTermicaAnnuale

    public void cittaCaldoFreddo(FileWriter fileWriter) throws IOException {
        String citta_max = "", citta_min = "", mese_max = "", mese_min = "";
        double max = Double.MIN_VALUE, min = Double.MAX_VALUE;

        for (String chiave : temperature_massime.keySet()) {
            for (Double temperatura : temperature_massime.get(chiave))
                if (temperatura > max) {
                    max = temperatura;
                    citta_max = Utilities.capitali.get(chiave.substring(3));
                    mese_max = Utilities.MESI[Integer.parseInt(chiave.substring(0, 2))-1];
                }//if

            for (Double temperatura : temperature_minime.get(chiave))
                if (temperatura < min) {
                    min = temperatura;
                    citta_min = Utilities.capitali.get(chiave.substring(3));
                    mese_min = Utilities.MESI[Integer.parseInt(chiave.substring(0, 2))-1];
                }//if

        }//for(chiave)
        fileWriter.write("max_country_state; max_month; max_temp; min_country_state; min_month; min_temp; avg_min_exc_month; avg_min_exc_temp; min_exc_month; min_exc_temp; avg_max_exc_month; avg_max_exc_temp; max_exc_month; max_exc_temp\n");
        fileWriter.write(String.format("%s; %s; %s; %s; %s; %s; ", citta_max, mese_max, (new DecimalFormat("0.00").format(max)).replace(',','.'),
                citta_min, mese_min, (new DecimalFormat("0.00").format(min)).replace(',','.')));
    }//cittaCaldoFreddo

    public void emettiTuple() {
        outputCollector.emit(new Values(temperature_massime, temperature_minime, temperature_medie));
    }//emettiTuple

    @Override
    public void prepare(Map<String, Object> map, TopologyContext topologyContext, OutputCollector outputCollector) {
        this.outputCollector = outputCollector;
    }//prepare

    @Override
    public void execute(Tuple tuple) {
        String citta = tuple.getStringByField("wban");
        String mese = tuple.getStringByField("mese");
        String temperatura_massima = tuple.getStringByField("tMax");
        String temperatura_minima = tuple.getStringByField("tMin");
        String temperatura_media = tuple.getStringByField("tAvg");

        String chiave = mese + "_" + citta;

        Utilities.aggiornaMappa(temperature_massime, chiave, temperatura_massima);
        Utilities.aggiornaMappa(temperature_minime, chiave, temperatura_minima);
        Utilities.aggiornaMappa(temperature_medie, chiave, temperatura_media);
        emettiTuple();
    }//execute

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
        outputFieldsDeclarer.declare(new Fields("temperature_massime", "temperature_minime", "temperature_medie"));
    }//declareOutputFields

    @Override
    public void cleanup() {
        //System.out.println(Utilities.mapToString(temperature_medie));
        try {
            FileWriter fileWriter= new FileWriter("risultati_temperature/2013_Temperature_Annuali.csv");
            fileWriter.write("mese; maxTemp; minTemp; avgTemp\n");

            for (int mese = 0; mese < Utilities.MESI.length; mese++) {
                FileWriter fileWriter1 = new FileWriter(String.format("risultati_temperature/2013_%s_Temperature.csv", Utilities.MESI[mese]));
                fileWriter1.write("avg_max_country_state; avg_max_temp; avg_min_country_state; avg_min_temp; max_max_country_state; max_max_temp; max_min_country_state; max_min_temp; min_max_country_state; min_max_temp; min_min_country_state; min_min_temp; avg_exc_temp; max_exc_temp; min_exc_temp\n");
                analisiMensile(temperature_medie, mese, "media", fileWriter1);
                analisiMensile(temperature_massime, mese, "massima", fileWriter1);
                analisiMensile(temperature_minime, mese, "minima", fileWriter1);
                calcolaEscursioneTermicaMensile(massime_medie, minime_medie, mese, fileWriter1);
                fileWriter1.close();

                sommaTemperatura(temperature_massime, temperature_minime, temperature_medie, mese, fileWriter);

                FileWriter fileWriter2 = new FileWriter(String.format("risultati_temperature/2013_%s_Medie_Temperature.csv", Utilities.MESI[mese]));
                fileWriter2.write("day; Tmax; Tmin; Tavg\n");
                scriviTemperatureMedie(fileWriter2, mese);
                fileWriter2.close();

            }//for
            fileWriter.close();
            FileWriter fileWriter3 = new FileWriter("risultati_temperature/2013_Temperature.csv");
            cittaCaldoFreddo(fileWriter3);
            calcolaEscursioneTermicaAnnuale(escursione_annuale, fileWriter3);
            fileWriter3.close();

        } catch (IOException e) {
            throw new RuntimeException(e);
        }//catch
    }//cleanup
}//class TemperaturaBolt
