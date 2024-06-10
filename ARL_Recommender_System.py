# İŞ PROBLEMİ

# Aşağıda 3 farklı kullanıcının sepet bilgileri verilmiştir. Bu sepet bilgilerine en uygun ürün önerisini birliktelik
# kuralı kullanarak yapınız. Ürün önerileri 1 tane ya da 1'den fazla olabilir. Karar kurallarını 2010-2011 Germany
# müşterileri üzerinden türetiniz. Kullanıcı 1’in sepetinde bulunan ürünün id'si: 21987 Kullanıcı 2’in sepetinde bulunan
# ürünün id'si : 23235 Kullanıcı 3’in sepetinde bulunan ürünün id'si : 22747

# Veri Seti Hikayesi

# Online Retail II isimli veri seti İngiltere merkezli bir perakende şirketinin 01/12/2009 - 09/12/2011 tarihleri
# arasındaki online satış işlemlerini içeriyor. Şirketin ürün kataloğunda hediyelik eşyalar yer almaktadır ve çoğu
# müşterisinin toptancı olduğu bilgisi mevcuttur.

# Değişkenler

# InvoiceNo = Fatura Numarası ( Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder )
# StockCode = Ürün kodu ( Her bir ürün için eşsiz )
# Description = Ürün ismi
# Quantity = Ürün adedi ( Faturalardaki ürünlerden kaçar tane satıldığı)
# InvoiceDate = Fatura tarihi
# UnitPrice = Fatura fiyatı ( Sterlin )
# CustomerID = Eşsiz müşteri numarası
# Country = Ülke ismi

# Proje Görevleri

# Görev 1: Veriyi Hazırlama

# Adım 1: Online Retail II veri setinden 2010-2011 sheet’ini okutunuz.

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)  # Çerçeve genişliğini ayarla
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_excel("ARL_Recommender_System/online_retail_II.xlsx",
                   sheet_name="Year 2010-2011")

# Adım 2: StockCode’u POST olan gözlem birimlerini drop ediniz. (POST her faturaya eklenen bedel, ürünü ifade etmemektedir.)

df = df[~df["StockCode"].str.contains("POST", na=False)]

# Adım 3: Boş değer içeren gözlem birimlerini drop ediniz.

df.isnull().sum()

# Adım 4: Invoice içerisinde C bulunan değerleri veri setinden çıkarınız. (C faturanın iptalini ifade etmektedir.)

df = df[~df["Invoice"].str.contains("C", na=False)]

# Adım 5: Price değeri sıfırdan küçük olan gözlem birimlerini filtreleyiniz.

df = df[df["Price"] > 0]

# Adım 6: Price ve Quantity değişkenlerinin aykırı değerlerini inceleyiniz, gerekirse baskılayınız.

df.describe().T

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

replace_with_thresholds(df, "Quantity")
replace_with_thresholds(df, "Price")

# Görev 2: Alman Müşteriler Üzerinden Birliktelik Kuralları Üretme

# Adım 1: Aşağıdaki gibi fatura ürün pivot table’i oluşturacak create_invoice_product_df fonksiyonunu tanımlayınız.

df_gr = df[df["Country"] == "Germany"]

def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', "Description"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)

gr_inv_pro_df = create_invoice_product_df(df_gr, id=True)


# Adım 2: Kuralları oluşturacak create_rules fonksiyonunu tanımlayınız ve alman müşteriler için kurallarını bulunuz.

frequent_itemsets = apriori(gr_inv_pro_df, min_support=0.01, use_colnames=True)
frequent_itemsets.sort_values("support", ascending=False)

rules = association_rules(frequent_itemsets,
                          metric="support",
                          min_threshold=0.01)

# Görev 2: Sepet İçerisindeki Ürün Id’leri Verilen Kullanıcılara Ürün Önerisinde Bulunma

# Adım 1: check_id fonksiyonunu kullanarak verilen ürünlerin isimlerini bulunuz.

def check_id(dataframe, id):
    product_name = dataframe[dataframe["StockCode"] == id][["Description"]].values[0].tolist()
    return product_name

# Adım 2: arl_recommender fonksiyonunu kullanarak 3 kullanıcı için ürün önerisinde bulununuz.

def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])
    return recommendation_list[0:rec_count]

check_id(df, 21987)

arl_recommender(rules, 21987, 5)

check_id(df, 23235)

arl_recommender(rules, 23235, 5)

check_id(df, 22747)

arl_recommender(rules, 22747, 5)

# Adım 3: Önerilecek ürünlerin isimlerine bakınız.

recommended_ids = arl_recommender(rules, 21987, 5)
product_names = [check_id(df, product_id) for product_id in recommended_ids]
recommended_ids = arl_recommender(rules, 23235, 5)
product_names = [check_id(df, product_id) for product_id in recommended_ids]
recommended_ids = arl_recommender(rules, 22747, 5)
product_names = [check_id(df, product_id) for product_id in recommended_ids]