package org.example.progetto.utils;

import com.opencsv.CSVReader;

import java.io.FileReader;
import java.text.DecimalFormat;
import java.util.*;

@SuppressWarnings("ALL")
public class Utilities {
    public static final String []MESI = {"Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"};
    public static Map<String, String> capitali = new HashMap<>();
    // private static final String PATH_CAPITALI = "dataset\\QCLCD\\wban_stato_capitale.csv";
    private static final String PATH_CAPITALI = "pathTo\\dataset\\QCLCD\\wban_stato_capitale.csv";

    public static String get_dataSet_path(String mese, String file_name) {
        //return "dataset\\QCLCD\\CSV2013" + mese + "\\2013" + mese + file_name;
        return "pathToYour\\dataset\\QCLCD\\CSV2013" + mese + "\\2013" + mese + file_name;

    }//get_dataSet_path

    public static String get_regression_path(String anno, String mese) {
        //return String.format("dataset\\RegressioneLineare\\%s\\%s%smonthly.csv", anno, anno, mese);
        return String.format("pathToYour\\dataset\\RegressioneLineare\\%s\\%s%smonthly.csv", anno, anno, mese);

    }//get_dataSet_path

    public static void aggiornaMappa(Map<String, Double> mappa, String chiave, double valore) {
        double nuovo_valore;
        if (!mappa.containsKey(chiave))
            nuovo_valore = valore;
        else
            nuovo_valore = mappa.get(chiave) + valore;
        mappa.put(chiave, nuovo_valore);
    }//aggiornaMappa

    public static void aggiornaMappa(Map<String, List<Double>> mappa, String chiave, String temperatura) {
        if (!temperatura.contains("M"))
            if (mappa.containsKey(chiave))
                mappa.get(chiave).add((Double.parseDouble(temperatura) - 32) / 1.8);
            else {
                List<Double> valori_temperatura = new LinkedList<>();
                valori_temperatura.add((Double.parseDouble(temperatura) - 32) / 1.8);
                mappa.put(chiave, valori_temperatura);
            }//else
    }//aggiornaMappa

    public static void riempiCapitali() throws Exception {
        CSVReader leggi_CSV = new CSVReader(new FileReader(PATH_CAPITALI));
        List<String[]> contenuto = leggi_CSV.readAll();
        for(String[] riga : contenuto)
            if(riga[0].length() == 5)
                capitali.put(riga[0], riga[3].trim() + ", " + riga[1].trim());
            else
                capitali.put("0" + riga[0], riga[3].trim() + ", " + riga[1].trim());
    }//riempiCapitali

    public static int contaGiorni(String mese){
        if(mese.equals("02") || mese.equalsIgnoreCase("Febbraio"))
            return 28;
        if(mese.equals("04") || mese.equals("06") || mese.equals("09") || mese.equals("11")
                || mese.equalsIgnoreCase("Aprile") || mese.equalsIgnoreCase("Giugno")||
                mese.equalsIgnoreCase("Settembre") || mese.equalsIgnoreCase("Novembre"))
            return 30;
        return 31;
    }//contaGiorni

    public static String mapToString(Map<?, ?> mappa){
        StringBuilder sb = new StringBuilder();
        for(Object chiave : mappa.keySet())
            sb.append(String.format("%s_%s",MESI[Integer.parseInt(String.valueOf(chiave).substring(0,2))-1],capitali.get(String.valueOf(chiave).substring(3))))
                    .append(" = ").append((List<Double>)mappa.get(chiave)).append("\n");
        return sb.toString();
    }//mapToString

    public static String mapToStringGiornaliera(Map<String, Double> mappa) {
        StringBuilder sb = new StringBuilder();
        for(Object chiave : mappa.keySet())
            sb.append(String.format("%s%s_%s",MESI[Integer.parseInt(String.valueOf(chiave).substring(0,2))-1], String.valueOf(chiave).substring(2,4),capitali.get(String.valueOf(chiave).substring(5))))
                    .append(" = ").append(new DecimalFormat("0.00").format(mappa.get(chiave))).append("\n");
        return sb.toString();
    }//mapToStringGiornaliera


}//class Utilities
