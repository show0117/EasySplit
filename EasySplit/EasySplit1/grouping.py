if __name__ == '__main__':
    # input setting
    in_dir = input("input the data source: \n")
    ot_dir = input("input the data destination: \n")
    group = int(input('input how many group should be divided: \n'))

    # read data
    import pandas as pd

    try:
        df = pd.read_csv(in_dir, encoding='big5')
    except:
        df = pd.read_csv(in_dir)

    # data to list
    name_list = list(df.iloc[:, 0])

    # covert to num
    df1 = pd.get_dummies(df.iloc[:, 1:])

    # hierarchy cluster
    import scipy
    import scipy.cluster.hierarchy as sch
    import numpy as np

    # clustering
    disMat = sch.distance.pdist(df1, 'euclidean')
    Z = sch.linkage(disMat, method = 'average')
    P = sch.dendrogram(Z, labels = name_list)
    ## plt.show()
    
    # team list
    if len(P['ivl']) % group == 0:
        temp = np.asarray(P['ivl'])
    else:
        temp = P['ivl'] + [''] * (group - len(P['ivl']) % group)
    temp = np.asarray(temp).reshape(int(len(temp) / group), group)

    # output data
    team_sheet = pd.DataFrame(temp)
    team_sheet.columns = ['team_' + str(i + 1) for i in range(group)]
    team_sheet.to_csv(ot_dir, encoding='utf-8-sig')
    print('Finished!!!! Please check your destination file~')
