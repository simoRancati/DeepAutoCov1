# DeepAutoCov
Code and data to reproduce the simulation in the following publication:

_Forecasting dominance of SARS-CoV-2 lineages by anomaly detection using deep AutoEncoders
Simone Rancati, Giovanna Nicora, Mattia Prosperi, Riccardo Bellazzi, Simone Marini, Marco Salemi
bioRxiv 2023.10.24.563721; doi: https://doi.org/10.1101/2023.10.24.563721_

Scripts to predict anomalies, i.e., Future Dominant Lineages (**FDLs**) with the Deep Learning AutoEncoder and to perform the simulation are located in the <code>model</code> folder.
Scripts to generate the dataset and the feature representations are within the <code>Feature_Extraction</code> folder.

## Feature Extraction
The file to create the dataset is <code>Data_filtration_kmers.py</code>. Example:
<code>python Data_Filtration_kmers.py -f Spikes_prova.fasta -c pseudodataset.csv -m 1000 -l 30 -p /path/to/save/dataset_interest_2023 </code>

Mandatory
-f: path where the input fasta file is stored (Example file: <code>data_github/Spikes_prova.fasta</code>).
-c: path where the input metadata (csv) is stored (Example file: <code>data_github/pseudodataset.csv</code>). Sequences and metadata should be in the same order. All columns are necessary and must be in the same order as in the example file, i.e.: <code> Virus name, Last vaccinated, Passage details/history, Type, Accession ID, Collection date, Location, Additional location information, Sequence length, Host, Patient age, Gender, Clade, Pango lineage, Pango version, Variant, AA Substitutions, Submission date, Is reference?, Is complete?, Is high coverage?, Is low coverage?, N-Content, GC-Content</code>

Optional
-n: nation (e.g., "France") (if not specified, all sequences are used) (<code>default: ['/']</code>);

-m: Filter: minimum lenght of the spike sequences (<code>default value: 1000</code>); 

-l: Filter: accepted amino acid distant from lineage median (<code>default value: 30</code>); as in: for each lineage, how the protein length can vary to be accepted?

-p: path to save the outputs.

-Output:
1) Metadata: Metadata of filtered sequences (<code>filtered_metadatataset</code>);
2) Dataset: It creates a folder (<code>dataset</code>) that contains subfolders (numbered by weeks <code>i.e; 1</code>). Each subfolder has:
  a) csv file for each sequence (<code>EPI_ISL_6331230.csv</code>).In the first raw contains all the k-mers possible.    The second, instead, contains a sequence of 0/1 that indicates the presence or absence of k-mers.
  b) txt File (<code>week_dataset.txt</code>) that contains the identificators and the sequence of 0/1

## Model prediction
The file to predict the anomalies and run the simulation is <code>Main_prediction_AE.py</code>. Example:
<code>python Main_prediction_AE.py -p /path/to/dataset/ -c /path/to/metadata.csv -k /path/to/kmers_file.csv -s /path/where/to/save/output -m 0.1 -e 300 -b 256 -d 1024 -r 1e-7 </code>

Mandatory:
-p path of dataset created during the feature extraction (<code>Exemple: /path/to/save/dataset/</code>);
-c path where <code>filtered_metadatataset</code> is stored (<code>Exemple: /path/to/metadata.csv </code>);
-k path where kmers are stored (example: first line of csv file created in subfolders <code>EPI_ISL_6331230.csv</code>).

Optional
-s path to save the outputs (<code>/path/to/save/drive_save</code>);
-m fraction of kmers that are different from 0 to mantain during the simulation (<code>default value: 0.05</code>);
-e number of epochs (<code>default value: 300</code>);
-b batch size for the first week (<code>default value: 256</code>);
-d Sets the encoding dimension (<code>default value: 1024</code>);
-r learning rate (<code>default value: 1e-7</code>).


-Output:
1) Precision-graph of the top 100 sequences with higer mean square error (mse) considereted as anomalies by DeepAutoCov model (<code>Fraction_general100</code>);
2) file.log containing for each week of simulation how many sequences the model identified like anomalies for each Future Dominant Lineage or FDL (<code>Autoencode_performance.log</code>);
3) Graph of the precision considering all the sequences considerated anomalies by DeepAutoCov model (<code>precision_overall.png</code>);
4) Graph F1,Precision,Recall (these graphs are as tests to see how the behaviour of model not considering the fact that the "Anomaly" class varies each time) (<code>precision_in_time.png</code>,<code>recall_in_time.png</code>,<code>f1_in_time</code>); 
5) File.h5 which contains the information (weights) of the trained AutoEncoder (<code>autoencoder_AERNS.h5</code>);
6) Graph of number of features (k-mers) during simulation (<code>number_of_features.png</code>);
7) file CSV that contains for each sequence analysed the k-mers not reproduced correctly by DeepAutoCov (The first column contain the id_sequence and other columns contain the k-mers not reproduced correctly) (<code>summary_kmers_week.csv</code>). 






