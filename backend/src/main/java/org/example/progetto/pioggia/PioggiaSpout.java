package org.example.progetto.pioggia;

import com.opencsv.CSVReader;
import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;
import org.example.progetto.utils.Utilities;

import java.io.FileReader;
import java.text.DecimalFormat;
import java.util.List;
import java.util.Map;

@SuppressWarnings("ALL")
public class PioggiaSpout extends BaseRichSpout {
    private SpoutOutputCollector spoutOutputCollector;
    private final String file_name;
    private boolean isCompleted;

    public PioggiaSpout(String file_name) {
        this.file_name = file_name;
    }//costruttore normale

    @Override
    public void open(Map<String, Object> map, TopologyContext topologyContext, SpoutOutputCollector spoutOutputCollector) {
        this.spoutOutputCollector = spoutOutputCollector;
    }//open

    @Override
    public void nextTuple() {
        if (!isCompleted) {
            for (int i = 0; i < Utilities.MESI.length; i++) {
                String path = Utilities.get_dataSet_path(new DecimalFormat("00").format(i + 1), file_name);
                try (CSVReader leggi_file = new CSVReader(new FileReader(path))) {
                    List<String[]> contenuto = leggi_file.readAll();
                    for (String[] riga : contenuto)
                        if (Utilities.capitali.containsKey(riga[0]))
                            spoutOutputCollector.emit(new Values(riga[0], riga[1].substring(4), riga[3]));
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }//catch
                isCompleted = true;
            }//for
        } else this.close();
    }//nextTuple

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
        outputFieldsDeclarer.declare(new Fields("wban", "mese_giorno", "pioggia"));
    }//declareOutputFields
}//classPioggiSpout
