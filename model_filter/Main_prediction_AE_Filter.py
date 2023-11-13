from load_data import *
from get_lineage_class import *
from map_lineage_to_finalclass import *
from optparse import OptionParser
from Autoencoder_training_GPU import *
import logging
from sklearn.model_selection import ParameterGrid
from fraction_mail_postfiltering import *
from barplot_laboratory import *
from Discovery import *
from filter_dataset import *
from test_normality_error import *
import gc
from model_dl import *
from Best_worse import *
from plot_smooth import *
from kmers_error import *
from Lookuptable import *
from Lineages_of_interest import *


def main(options):

    ## Memory Control
    gc.enable()

    ## GPU
    strategy = tf.distribute.MirroredStrategy()

    ## Definition of a list for utilization throughout the code.

    number_week_nseq = []  # A list to store predictions for each lineage and for each week.
    prediction_lineages = []
    summary_lineages = []  # A list to store a summary for each lineage and for each week.
    number_of_feature = []  # Number of features.
    results_fine_tune = []
    fractions_100 = [] # A list to store predictions for the top 100 sequences with higher mean squared error (MSE).
    ind_prc = 0 # Counter
    summary_100_anomalies = [] # List containing the number of sequences considered as anomalies for each lineage and for each week of simulation.
    summary_100_anomalies_percentage = [] # List containing the percentage of sequences considered as anomalies for each lineage and for each week of simulation.

    ## Path to read the dataset

    dir_week =str(options.path_drive) # Path dataset generated by Data_Filtration_kmers.py.

    metadata = pd.read_csv(str(options.csv_path)) # Read metadata filtered file generated by Data_Filtration_kmers.py
    metadata_2 = pd.read_csv(str(options.csv_path)) # Read metadata filtered file generated by Data_Filtration_kmers.py


    ## Columns in metadata
    col_class_lineage = 'Pango.lineage'
    col_submission_date = 'Collection.date'
    col_lineage_id = 'Accession.ID'

    ## Processing of Data
    valid_lineage, valid_lineage_prc, dizionario_lineage_settimane, lineages_know = lineages_of_interest() # Function that return the Future Dominant Lineages (FDLs) of Interest.

    metadata[col_class_lineage] = metadata[col_class_lineage].apply(lambda x: 'unknown' if x not in valid_lineage else x) # Replacement of non-FDLs by unknown.

    ## Retraining Week
    retraining_week, retraining_week_false_positive = retraining_weeks() # Return retraining weeks.

    ## K-mers
    header = pd.read_csv(str(options.kmers), nrows=1)
    features = header.columns[1:].tolist()  # k-mers
    print('-----------------------------------------------------------------------------------')
    print('The total number of k-mers is : ' + str(len(features)))
    print('-----------------------------------------------------------------------------------')

    path_save_file=str(options.path_save) # path to save the outputs.

    ## Lineage of interest
    lineage_of_interest = metadata[col_class_lineage].unique().tolist() # Return the FDLs present in the dataset.
    lineage_of_interest.remove('unknown')


    ## Logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            # logging.FileHandler('/mnt/resources/2022_04/2022_04/'+'run_main_oneclass_retrain_tmp.log', 'w+'),
                            logging.FileHandler(path_save_file + '/Autoencode_performance.log', 'w+'),
                            logging.StreamHandler()
                        ])


    ## Training week
    starting_week = 1 # First week of training.

    ## Loading first training set
    df_trainstep_1, train_w_list = load_data(dir_week, [starting_week]) # First training set.
    train_step1 = df_trainstep_1.iloc[:, 1:len(df_trainstep_1.columns)].to_numpy()

    ## Filter the features of models
    sum_train = np.sum(train_step1, axis=0)
    keepFeature=sum_train/len(train_step1)
    i_no_zero = np.where(keepFeature >= options.rate_mantain)[0] # Retain the features that differ from 0 by at least N%. This approach ensures that only the most representative features are kept.

    print('---------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('The features of the model are :' + str((len(i_no_zero))))
    print('---------------------------------------------------------------------------------------------------------------------------------------------------------')

    ## Training set
    y_train_initial = metadata[metadata[col_lineage_id].isin(df_trainstep_1.iloc[:, 0].tolist())][col_class_lineage] # Elements of training set.
    y_train_class = map_lineage_to_finalclass(y_train_initial.tolist(), lineage_of_interest)  # Class of training set.
    counter_i = Counter(y_train_initial)

    ## Filtering out features with all zero
    train_step_complete_rw = train_step1
    train = train_step1[:, i_no_zero] # Select the representative features.
    lineages_train=np.array(y_train_initial.tolist()) # Type of lineages.

    tf.random.set_seed(10)
    ## Creation of  Autoencoder models

    # Parameters
    nb_epoch = options.number_epoch
    batch_size = options.batch_size
    input_dim =train.shape[1]
    encoding_dim = options.encoding_dim
    hidden_dim_1 = int(encoding_dim / 2)
    hidden_dim_2=int(hidden_dim_1/2)
    hidden_dim_3=int(hidden_dim_2/2)
    hidden_dim_4=int(hidden_dim_3/2)
    hidden_dim_5=int(hidden_dim_4/2)
    reduction_factor = options.red_factor

    p_grid = {'nb_epoch':[nb_epoch],'batch_size':[batch_size],'input_dim':[input_dim],'encoding_dim':[encoding_dim],'hidden_dim_1':[int(encoding_dim / 2)],'hidden_dim_2':[hidden_dim_2],'hidden_dim_3':[hidden_dim_3],'hidden_dim_4':[hidden_dim_4],'hidden_dim_5':[hidden_dim_5],'Reduction_factor':[reduction_factor]}
    all_combo = list(ParameterGrid(p_grid))

    with strategy.scope(): # Using GPU
        autoencoder=model(input_dim,encoding_dim,hidden_dim_1,hidden_dim_2,hidden_dim_3,hidden_dim_4,hidden_dim_5,reduction_factor,path_save_file) # Project the Deep Learning Model.
    for combo in all_combo[0:1]:
        combo
        logging.info("---> Autoencoder - Param: " + str(combo))
        y_test_dict_variant_type = {}
        y_test_dict_finalclass = {}
        y_test_dict_predictedclass = {}
        history = autoencoder_training_GPU(autoencoder,train, train,nb_epoch,batch_size) # Training the model.
        autoencoder.save(path_save_file+'/Autoencoder_models.h5') # saving model in h5 format.
        print('The model is trained !')
        print(history)
        info, mse_tr = test_normality(autoencoder, train) # Compute the MSE in the training set. This is important to define the threshold for the anomaly detetction.
        ## SIMULATION
        for week in range(1, 159): # Simulation weeks
            if week in retraining_week:
                logging.info('----> RETRAINING <-----')
                ind_prc = ind_prc + 1

                # We create a new training set for retrain the network
                train_model_value = train_step_complete_rw # soloziono solo i kmaers
                classi=lineages_train #seleziono solo i valori
                sum_train = np.sum(train_model_value, axis=0)
                keepFeature = sum_train / len(train_model_value)
                i_no_zero = np.where(keepFeature > options.rate_mantain)[0]

                number_feature = len(i_no_zero)
                print('---------------------------------------------------------------------------------------------------------------------------------------------------------')
                print('il numero di feature in almeno il 5% delle sequenze diverso da zero sono :' + str((len(i_no_zero))))
                print('---------------------------------------------------------------------------------------------------------------------------------------------------------')

                train_model_value = train_model_value[:, i_no_zero]

                # seleziono le righe di interesse
                index_raw = trova_indici_lineage_per_settimana(classi, week, dizionario_lineage_settimane) # prende in ingresso solo le classi
                train_model_value=train_model_value[index_raw,:]
                np.random.shuffle(train_model_value)
                number_of_feature.append(number_feature)

                batch_size=512
                input_dim =train_model_value.shape[1]
                with strategy.scope():
                    autoencoder=model(input_dim, encoding_dim, hidden_dim_1, hidden_dim_2, hidden_dim_3, hidden_dim_4, hidden_dim_5,
                          reduction_factor, path_save_file)
                history = autoencoder_training_GPU(autoencoder, train_model_value, train_model_value, nb_epoch, batch_size)

                print('Ho allenato la rete neurale : ')
                print(history)

                info,mse_tr = test_normality(autoencoder, train_model_value)
                train_model_value = []
                classi=[]
            logging.info("# Week " + str(starting_week + week))
            print("# Week " + str(starting_week + week))

            ## Loading test set
            # Download test set from the folder created in the script "Data_Filtration_kmers"
            df_teststep_i, test_w_list = load_data(dir_week, [starting_week + week]) # Test set.
            test_step_i = df_teststep_i.iloc[:, 1:len(df_teststep_i.columns)].to_numpy() # transform in numpy.
            id_identifier = df_teststep_i.iloc[:, 0].to_list() # Sequence Identifier.
            test_step_complete_rw = test_step_i # (rw = retraining week)
            test_step_i = test_step_i[:, i_no_zero] # feature selections
            y_test_step_i = get_lineage_class(metadata, df_teststep_i.iloc[:, 0].tolist()) # type of lineages present in test set.
            lineages_l=metadata[metadata[col_lineage_id].isin(df_teststep_i.iloc[:, 0].tolist())][col_class_lineage] # Type of lineages in the week of simulation.
            lineages_test=np.array(lineages_l.tolist()) # lineages in the week [array]
            #test_with_class_completo = np.column_stack((test_step_completo, lineages))
            y_test_dict_variant_type[starting_week + week] = y_test_step_i
            y_test_fclass_i = map_lineage_to_finalclass(y_test_step_i, lineage_of_interest)  # return the class of sequences present in the test set. (-1->FDLs, 1->No FDLs).
            i_voc = np.where(np.array(y_test_fclass_i) == -1)[0]
            y_test_dict_finalclass[starting_week + week] = y_test_fclass_i
            lineage_dict = Counter(y_test_step_i) # Dictionary that contains the lineages present in the test set.

            ## Model Prediction
            test_x_predictions = autoencoder.predict(test_step_i) # predictions

            ## Threshold
            mse = np.mean(np.power(test_step_i - test_x_predictions, 2), axis=1) # Mean Square Error (MSE).
            error_df = pd.DataFrame({'Reconstruction_error': mse})
            threshold_fixed = np.mean(mse_tr) + 1.5 * np.std(mse_tr) # Threshold for anomaly detection.
            print('Threshold is : ' + str(threshold_fixed))
            y_test_i_predict = [-1 if e >= threshold_fixed else 1 for e in error_df.Reconstruction_error.values]
            y_test_i_predict = np.array(y_test_i_predict)

            ## Filter
            y_test_i_predict, mse = lookup(y_test_i_predict, y_test_step_i, lineages_know[ind_prc], mse)

            ## Selection the first 100 sequences with highest mse
            TP_100, FP_100, N_100 =  Top100(list(mse), y_test_step_i, week, threshold_fixed, 100, lineages_know[ind_prc])
            fractions_100.append([TP_100, FP_100, N_100])

            # Graphs
            graphic_fraction(fractions_100, 100, path_save_file)

            ## The k-mers importance
            i_anomaly = np.where(y_test_i_predict == -1)[0]
            features_no_zero = [features[i] for i in i_no_zero] # features of model
            selection_kmers(test_x_predictions, test_step_i, features_no_zero, y_test_i_predict, id_identifier,'Summary_'+str(starting_week+week)+'.csv') # this function identifies kmers that have not been reproduced correctly by the model.

            ## Undestand the error and save the outputs

            lineages_error = metadata_2[metadata_2[col_lineage_id].isin(df_teststep_i.iloc[:, 0].tolist())][
                col_class_lineage]  # Important to define the top 100 anomalies.
            lineages_error_test = np.array(lineages_error.tolist())

            # Selection of sequences considered as anomalies by the model.
            mse_top100_anomaly = mse[i_anomaly]
            lineage_top100_anomaly = lineages_error_test[i_anomaly]

            # Select the top 100 and sort mse
            size = 100
            if len(i_anomaly) < 100:
                size = len(i_anomaly)
            top_indices_100 = mse_top100_anomaly.argsort()[-size:][::-1] # sort the MSE
            lineages_predicted_top_100 = lineage_top100_anomaly[top_indices_100]

            # Filtering with the biological knowledge (double check)
            prediction = list(-np.ones(size))
            prediction_filtering = lookup_post(prediction, lineages_predicted_top_100, lineages_know[ind_prc]) # Filter the prediction

            # Find the anomalies after filtering
            prediction_filtering = np.array(prediction_filtering)
            index_anomaly_filter = np.where(prediction_filtering == -1)[0] # Find the anomalies.
            lineages_predicted_top_100 = lineages_predicted_top_100[index_anomaly_filter]
            lineages_counter_top_100 = Counter(lineages_predicted_top_100) # Count the anomalies identified by the model
            total_100 = sum(lineages_counter_top_100.values())
            lineage_percentage_100 = {k: (v / total_100) * 100 for k, v in lineages_counter_top_100.items()}

            # list prediction during the simulation week
            summary_100_anomalies.append([week,lineages_counter_top_100])
            summary_100_anomalies_percentage.append([week,lineage_percentage_100])

            # Write the file in txt the prediction
            with open(path_save_file+'/TOP_100_FILTERING.txt', 'w') as file:
                # Scrivi ogni elemento della lista in una nuova riga nel file
                for elemento in summary_100_anomalies:
                    file.write(str(elemento) + '\n')

            # Write the file in txt the prediction precision
            with open(path_save_file + '/TOP_100_FILTERING_PERCENTAGE.txt', 'w') as file:
                # Scrivi ogni elemento della lista in una nuova riga nel file
                for elemento in summary_100_anomalies_percentage:
                    file.write(str(elemento) + '\n')

            # Training set for retraining
            train_step_complete_rw=np.concatenate((train_step_complete_rw, test_step_complete_rw)) # (rw = retraining week)
            lineages_train=np.concatenate((lineages_train, lineages_test)) # list that contains the lineages present in training set
            y_test_dict_predictedclass[starting_week + week] = y_test_i_predict
            y_test_voc_predict = np.array(y_test_i_predict)[i_voc]

            logging.info("Number of lineage in week:" + str(test_step_i.shape[0]))
            print("Number of lineage in week:" + str(test_step_i.shape[0]))
            logging.info("Number of lineage of concern in week:" + str(len([x for x in y_test_fclass_i if x == -1])))
            print("Number of lineage of concern in week:" + str(len([x for x in y_test_fclass_i if x == -1])))
            logging.info("Distribution of lineage of concern:" + str(Counter(y_test_step_i)))
            print("Distribution of lineage of concern:" + str(Counter(y_test_step_i)))
            logging.info("Number of lineage predicted as anomalty:" + str(
            len([x for x in y_test_dict_predictedclass[starting_week + week] if x == -1])))
            print("Number of lineage predicted as anomalty:" + str(
                len([x for x in y_test_dict_predictedclass[starting_week + week] if x == -1])))
            acc_voc = len([x for x in y_test_voc_predict if x == -1])
            logging.info("Number of lineages of concern predicted as anomalty:" + str(acc_voc))
            print("Number of lineages of concern predicted as anomalty:" + str(acc_voc))

            for k in lineage_dict.keys():
                i_k = np.where(np.array(y_test_step_i) == k)[0]
                logging.info('Number of ' + k + ' lineage:' + str(len(i_k)) + '; predicted anomalty=' + str(
                    len([x for x in y_test_i_predict[i_k] if x == -1])))
                print('Number of ' + k + ' lineage:' + str(len(i_k)) + '; predicted anomalty=' + str(
                    len([x for x in y_test_i_predict[i_k] if x == -1])))
                # Store the file.
                h = len([x for x in y_test_i_predict[i_k] if x == -1])
                partial_summary = [k, h, week] # The list contains : [Name of lineage, Number of lineage sequences predicted as anomalies, week of simulation].
                prediction_lineages.append(partial_summary) # Store the partial summary
                complete_summary_lineages = [k, len(i_k), h, week]  # The list contains : [Name of lineage,Total number of lineage sequences in the week of simulation,Number of lineage sequences predicted as anomalies, week of simulation].
                summary_lineages.append(complete_summary_lineages) # Store complete summary.


        # saving results for this comb of param of the oneclass_svm
        results = {'y_test_variant_type': y_test_dict_variant_type,
               'y_test_final_class': y_test_dict_finalclass,
               'y_test_predicted_class': y_test_dict_predictedclass}
    results_fine_tune.append(results)

    print('---------------------------------Vector of predictions total----------------------------------------------------------------')
    print(summary_100_anomalies)
    print('---------------------------------Vector of predictions percentage----------------------------------------------------------------')
    print(summary_100_anomalies_percentage)
    print('---------------------------------Fractions top 100---------------------------------------------------------------------------')
    print(fractions_100)
    print('----------------------------------------------------------------------------------------------------------------------------')

    ## THE BEST AND WORST
    best_worst(path_save_file) # World case

    ## Week before
    distance=weeks_before(summary_lineages)
    distance_np=np.array(distance)
    distance_list = list(distance_np)
    with open(path_save_file + '/distance_prediction.txt', 'w') as file:
        for elemento in distance_list:
            file.write(str(elemento) + '\n')
    print('-----------------------------------------Prediction weeks before threshold-------------------------------------------------------')
    print(distance_np)
    print('---------------------------------------------------------------------------------------------------------------------------')

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-p", "--pathdrive", dest="path_drive",

                      help="path to drive example: path/drive/", default="/blue/salemi/share/varcovid/dataset_febb_2023_little/")   # default
    parser.add_option("-c", "--csv", dest="csv_path",

                      help="path to CSV file metadata", default="/blue/salemi/share/varcovid/filtered_metadatataset_010223_edit_200323.csv")

    parser.add_option("-k","--kmers",dest="kmers",
                      help="path of file kmers",default='/blue/salemi/share/varcovid/dataset_febb_2023_little/1/EPI_ISL_14307752.csv')

    parser.add_option("-s", "--pathsave ", dest="path_save",
                      help="path where we can save the file", default='/blue/salemi/share/varcovid/PAPAER_GROSSO/RISULTATI/WORLD_25_TH')

    parser.add_option("-m", "--mantain ", dest="rate_mantain",
                      help="rate for mantain the k-mers", default=0.05)

    parser.add_option("-e", "--Epoch ", dest="number_epoch",
                      help="number of epochs", default=10)

    parser.add_option("-b", "--Batchsize ", dest="batch_size",
                      help="number of batchsize in the first week", default=256)

    parser.add_option("-d", "--encoding dimension ", dest="encoding_dim",
                      help="encodin dimention", default=1024)

    parser.add_option("-r", "--reduction facor ", dest="red_factor",
                      help="red_factor", default=1e-7)

    (options, args) = parser.parse_args()
    main(options)
