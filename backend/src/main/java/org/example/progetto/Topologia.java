package org.example.progetto;

import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.StormSubmitter;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.tuple.Fields;
import org.example.progetto.citta.CittaBolt;
import org.example.progetto.pioggia.PioggiaBolt;
import org.example.progetto.pioggia.PioggiaSpout;
import org.example.progetto.regressione_lineare.RegressioneBolt;
import org.example.progetto.regressione_lineare.RegressioneSpout;
import org.example.progetto.temperatura.TemperaturaBolt;
import org.example.progetto.temperatura.TemperaturaSpout;
import org.example.progetto.utils.Utilities;

@SuppressWarnings("ALL")
public class Topologia {
    public static void esegui_pioggia(Config config, TopologyBuilder topologyBuilder) {
        topologyBuilder.setSpout("pioggia_spout", new PioggiaSpout("precip_part_1.csv"));
        topologyBuilder.setSpout("pioggia_spout1", new PioggiaSpout("precip_part_2.csv"));

        topologyBuilder.setBolt("pioggia_bolt", new PioggiaBolt(), 1)
                .fieldsGrouping("pioggia_spout", new Fields("wban"))
                .fieldsGrouping("pioggia_spout1", new Fields("wban"));
        config.setDebug(false);
    }//esegui_pioggia

    public static void esegui_temperatura(Config config, TopologyBuilder topologyBuilder) {
        topologyBuilder.setSpout("temperatura_spout", new TemperaturaSpout("daily.csv"));
        topologyBuilder.setBolt("temperatura_bolt", new TemperaturaBolt(), 1)
                .fieldsGrouping("temperatura_spout", new Fields("wban"));
        config.setDebug(false);
    }//esegui_pioggia

    public static void esegui_citta(Config config, TopologyBuilder topologyBuilder){
        topologyBuilder.setBolt("citta_bolt", new CittaBolt(), 1)
                .fieldsGrouping("pioggia_bolt", new Fields("pioggia_mesi"))
                .fieldsGrouping("temperatura_bolt", new Fields("temperature_massime"));
        config.setDebug(false);
    }//esegui_citta

    public static void esegui_regressione(Config config, TopologyBuilder topologyBuilder){
        topologyBuilder.setSpout("regressione_spout", new RegressioneSpout());

        topologyBuilder.setBolt("regressione_bolt", new RegressioneBolt(), 1)
                .fieldsGrouping("regressione_spout", new Fields("anno_mese"));


        config.setDebug(false);
    }//esegui_regressione
    public static void main(String... args) throws Exception {

        Utilities.riempiCapitali(); // metodo che serve a popolare la mappa delle 49 città capitali dell'america considerate nelle nostre analisi

        Config config = new Config();
        TopologyBuilder topologyBuilder = new TopologyBuilder();

        esegui_pioggia(config, topologyBuilder);
        esegui_temperatura(config, topologyBuilder);
        esegui_citta(config, topologyBuilder);
        esegui_regressione(config, topologyBuilder);
        if (args != null && args.length > 0)
            StormSubmitter.submitTopologyWithProgressBar(args[0], config, topologyBuilder.createTopology());
        else {
            LocalCluster localCluster = new LocalCluster();
            localCluster.submitTopology("weather_topology", config, topologyBuilder.createTopology());
            Thread.sleep(30000);
            localCluster.shutdown();
        }//else
        System.exit(0);
    }//main
}//class Topologia
