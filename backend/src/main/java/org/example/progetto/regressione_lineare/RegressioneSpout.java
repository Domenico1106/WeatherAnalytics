package org.example.progetto.regressione_lineare;

import com.opencsv.CSVReader;
import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;
import org.example.progetto.utils.Utilities;

import java.io.FileReader;
import java.util.List;
import java.util.Map;

public class RegressioneSpout extends BaseRichSpout {
    private SpoutOutputCollector spoutOutputCollector;
    private boolean isCompleted;
    @Override
    public void open(Map<String, Object> map, TopologyContext topologyContext, SpoutOutputCollector spoutOutputCollector) {
        this.spoutOutputCollector = spoutOutputCollector;
    }//open

    @Override
    public void nextTuple() {
        if(!isCompleted) {

            for(int anno = 2010; anno <= 2014; anno++) {
                for (int mese = 1; mese <= Utilities.MESI.length; mese++) {
                    String path = Utilities.get_regression_path(String.valueOf(anno) , String.format("%02d", mese));
                    try (CSVReader leggi_file = new CSVReader(new FileReader(path))) {
                        List<String[]> contenuto = leggi_file.readAll();
                        for (String[] riga : contenuto)
                            if (Utilities.capitali.containsKey(riga[0]))
                                spoutOutputCollector.emit(new Values(riga[1], riga[6]));
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }//catch
                }
                isCompleted = true;
            }
        } else this.close();
    }//nextTuple

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
        outputFieldsDeclarer.declare(new Fields("anno_mese", "avg_temp"));
    }//declareOutputFields
}//class RegressioneSpout
