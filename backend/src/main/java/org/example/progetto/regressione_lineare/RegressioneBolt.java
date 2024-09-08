package org.example.progetto.regressione_lineare;
import com.opencsv.CSVReader;
import org.apache.commons.math3.stat.regression.SimpleRegression;
import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;
import org.example.progetto.utils.Utilities;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.*;

@SuppressWarnings("ALL")
public class RegressioneBolt extends BaseRichBolt {

    private final Map<String, Double> temperatura_media = new HashMap<>();
    private final Map<String, List<Double>> mese_temp = new HashMap<>();


    public void updateMap(Map<String, Double> mappa, String chiave, double valore){
        double celsius = (valore-32) / 1.8;

        if (mappa.containsKey(chiave))
            mappa.put(chiave, mappa.get(chiave)+celsius);
        else mappa.put(chiave, celsius);
    }//updateMap

    @Override
    public void prepare(Map<String, Object> map, TopologyContext topologyContext, OutputCollector outputCollector) {

    }//prepare

    @Override
    public void execute(Tuple tuple) {
        String anno_mese = tuple.getStringByField("anno_mese");
        String avg_temp = tuple.getStringByField("avg_temp");

        if(!avg_temp.contains("M"))
            updateMap(temperatura_media, anno_mese, (Double.parseDouble(avg_temp)));
    }//execute

    private void popolaMappa() {
        for (int anno = 2010; anno <= 2014; anno++)
            for (int mese = 1; mese <= Utilities.MESI.length; mese++)
                if (mese_temp.containsKey(String.format("%02d", mese)))
                    mese_temp.get(String.format("%02d", mese)).add(temperatura_media.get(anno + String.format("%02d", mese))/49);
                else {
                    List<Double> l = new LinkedList<>();
                    l.add(temperatura_media.get(anno + String.format("%02d", mese))/49);
                    mese_temp.put(String.format("%02d", mese), l);
                }// else

    }// popolaMappa

    private void eseguiRegressioneLineare() throws IOException {
        double [] predizioni = new double[12];
        double [] anni = {2010, 2011, 2012, 2013};
        SimpleRegression simple_regression_monthly = new SimpleRegression(), simple_regression_yearly = new SimpleRegression();
        double valore_reale = 13.11;
        for (String chiave : mese_temp.keySet()) {
            for (int i = 0; i < 4; i++)
                simple_regression_monthly.addData(anni[i], mese_temp.get(chiave).get(i));
            predizioni[Integer.parseInt(chiave) - 1] = simple_regression_monthly.predict(2014);
            simple_regression_monthly = new SimpleRegression();
        }// for-each

        try (CSVReader leggi_file = new CSVReader(new FileReader("dataset\\RegressioneLineare\\TemperatureUSA.csv"))) {
            List<String[]> contenuto = leggi_file.readAll();
            for (String[] riga : contenuto)
                simple_regression_yearly.addData(Double.parseDouble(riga[0]), (Double.parseDouble(riga[1])-32)/1.8);
        }catch (Exception e){
            throw new RuntimeException();
        }// catch


        FileWriter fileWriter = new FileWriter("risultati_regressione/2014_Previsione.csv");
        fileWriter.write("mese; previsione; valoriReali; previsioneAnnuale; valoreAnnualeReali\n");
        for(int mese = 0; mese < 12; mese++)
            if (mese == 0)
                fileWriter.write(String.format("%s; %s; %s; %s; %s\n", Utilities.MESI[mese], new DecimalFormat("0.00").format(predizioni[mese]).replace(",", "."),
                        new DecimalFormat("0.00").format(mese_temp.get(String.format("%02d", mese + 1)).get(4)).replace(",", "."),
                        new DecimalFormat("0.00").format(simple_regression_yearly.predict(2014)).replace(",", "."),
                        new DecimalFormat("0.00").format(valore_reale).replace(",", ".")));
            else
                fileWriter.write(String.format("%s; %s; %s\n", Utilities.MESI[mese],new DecimalFormat("0.00").format(predizioni[mese]).replace(",", "."),
                        new DecimalFormat("0.00").format(mese_temp.get(String.format("%02d", mese + 1)).get(4)).replace(",", ".")));
        fileWriter.close();
    }// eseguiRegressioneLineare

    @Override
    public void cleanup() {
        popolaMappa();
        System.out.println(mese_temp.entrySet());
        try{
            eseguiRegressioneLineare();
        }catch (IOException e){
            System.out.println(e);
        }//catch
    }//cleanup

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {}//declareOutputFields
}// class RegressioneBolt
