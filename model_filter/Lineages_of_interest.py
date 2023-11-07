
def lineages_of_interest():
    valid_lineage = ['B.1.177', 'B.1', 'B.1.2', 'B.1.1', 'B.1.1.7', 'AY.103', 'AY.44', 'AY.43', 'AY.4', 'B.1.617.2',
                 'BA.2.12.1', 'BA.2', 'BA.1', 'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5',
                 'CH.1.1']

    valid_lineage_prc = [
    ['B.1.177', 'B.1', 'B.1.2', 'B.1.1', 'B.1.1.7', 'AY.103', 'AY.44', 'AY.43', 'AY.4', 'B.1.617.2', 'BA.2.12.1',
     'BA.2', 'BA.1', 'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['B.1.177', 'B.1.2', 'B.1', 'B.1.1.7', 'AY.103', 'AY.44', 'AY.43', 'AY.4', 'B.1.617.2', 'BA.2.12.1', 'BA.2', 'BA.1',
     'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['B.1.177', 'B.1.2', 'B.1.1.7', 'AY.103', 'AY.44', 'AY.43', 'AY.4', 'B.1.617.2', 'BA.2.12.1', 'BA.2', 'BA.1',
     'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['B.1.2', 'B.1.1.7', 'AY.103', 'AY.44', 'AY.43', 'AY.4', 'B.1.617.2', 'BA.2.12.1', 'BA.2', 'BA.1', 'BA.2.9',
     'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['B.1.1.7', 'AY.103', 'AY.44', 'AY.43', 'AY.4', 'B.1.617.2', 'BA.2.12.1', 'BA.2', 'BA.1', 'BA.2.9', 'BA.2.3',
     'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['AY.103', 'AY.44', 'AY.43', 'AY.4', 'B.1.617.2', 'BA.2.12.1', 'BA.2', 'BA.1', 'BA.2.9', 'BA.2.3', 'BA.5.1',
     'XBB.1.5', 'CH.1.1'],
    ['AY.103', 'AY.44', 'AY.43', 'B.1.617.2', 'BA.2.12.1', 'BA.2', 'BA.1', 'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5',
     'CH.1.1'],
    ['AY.103', 'AY.43', 'B.1.617.2', 'BA.2.12.1', 'BA.2', 'BA.1', 'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['AY.43', 'B.1.617.2', 'BA.2.12.1', 'BA.2', 'BA.1', 'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['AY.43', 'BA.2.12.1', 'BA.2', 'BA.1', 'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['BA.2.12.1', 'BA.2', 'BA.1', 'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['BA.2.12.1', 'BA.2', 'BA.2.9', 'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['BA.2.12.1', 'BA.2.3', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['BA.2.12.1', 'BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['BA.5.1', 'XBB.1.5', 'CH.1.1'],
    ['XBB.1.5', 'CH.1.1'],
    ['XBB.1.5'],
    []]

    dizionario_lineage_settimane = {
        10: ['unknown', 'B.1.1'],
        11: ['unknown', 'B.1', 'B.1.1'],
        44: ['unknown', 'B.1', 'B.1.1', 'B.1.177'],
        47: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177'],
        56: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7'],
        79: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4'],
        82: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'AY.44'],
        84: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'AY.44', 'AY.103'],
        87: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.44', 'AY.103'],
        105: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44',
              'AY.103'],
        107: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1'],
        111: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9'],
        121: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3'],
        126: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3', 'BA.2.12.1'],
        134: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3', 'BA.2.12.1', 'BA.5.1'],
        156: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3', 'BA.2.12.1', 'BA.5.1', 'CH.1.1'],
        159: ['unknown', 'B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3', 'BA.2.12.1', 'BA.5.1', 'CH.1.1', 'XBB.1.5'],
    }

    lineage_know = [[],['B.1.1'],['B.1', 'B.1.1'],['B.1', 'B.1.1', 'B.1.177'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'AY.44'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'AY.44', 'AY.103'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.44', 'AY.103'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44',
              'AY.103'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3', 'BA.2.12.1'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3', 'BA.2.12.1', 'BA.5.1'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3', 'BA.2.12.1', 'BA.5.1', 'CH.1.1'],['B.1', 'B.1.1', 'B.1.2', 'B.1.177', 'B.1.1.7', 'AY.4', 'B.1.617.2', 'AY.43', 'AY.44', 'AY.103',
              'BA.1', 'BA.2', 'BA.2.9', 'BA.2.3', 'BA.2.12.1', 'BA.5.1', 'CH.1.1', 'XBB.1.5']]
    return valid_lineage,valid_lineage_prc,dizionario_lineage_settimane,lineage_know

def retraining_weeks():
    retraining_week = [10, 11, 44, 47, 56, 79, 82, 84, 87, 105, 107, 111, 121, 126, 134, 156, 159]
    retraining_week_false_positive = [10, 11, 44, 47, 56, 79, 82, 84, 87, 105, 107, 111, 121, 126, 134, 156, 159, 160]
    return retraining_week,retraining_week_false_positive