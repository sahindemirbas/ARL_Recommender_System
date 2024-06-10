Product Recommendation System using Association Rules

İş Problemi

Bu proje kapsamında, üç farklı kullanıcının sepet bilgileri kullanılarak, birliktelik kuralları (association rules) aracılığıyla en uygun ürün önerilerinde bulunulacaktır. Öneriler, 2010-2011 yıllarına ait Almanya müşterileri üzerinden türetilecektir.

	•	Kullanıcı 1’in sepetinde bulunan ürünün ID’si: 21987
	•	Kullanıcı 2’in sepetinde bulunan ürünün ID’si: 23235
	•	Kullanıcı 3’in sepetinde bulunan ürünün ID’si: 22747

Veri Seti Hikayesi

Online Retail II isimli veri seti, İngiltere merkezli bir perakende şirketinin 01/12/2009 - 09/12/2011 tarihleri arasındaki online satış işlemlerini içermektedir. Şirketin ürün kataloğunda hediyelik eşyalar yer almakta ve çoğu müşterisinin toptancı olduğu bilinmektedir.

Değişkenler

	•	InvoiceNo: Fatura Numarası (Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder)
	•	StockCode: Ürün kodu (Her bir ürün için eşsiz)
	•	Description: Ürün ismi
	•	Quantity: Ürün adedi (Faturalardaki ürünlerden kaçar tane satıldığı)
	•	InvoiceDate: Fatura tarihi
	•	UnitPrice: Fatura fiyatı (Sterlin)
	•	CustomerID: Eşsiz müşteri numarası
	•	Country: Ülke ismi

Proje Görevleri

Görev 1: Veriyi Hazırlama

	1.	Online Retail II veri setinden 2010-2011 sheet’ini okutma.
	2.	“StockCode”u POST olan gözlem birimlerini çıkarma.
	3.	Boş değer içeren gözlem birimlerini çıkarma.
	4.	“Invoice” içerisinde C bulunan değerleri çıkarma.
	5.	“Price” değeri sıfırdan küçük olan gözlem birimlerini filtreleme.
	6.	“Price” ve “Quantity” değişkenlerinin aykırı değerlerini inceleyip, gerekirse baskılama.

Görev 2: Alman Müşteriler Üzerinden Birliktelik Kuralları Üretme

	1.	Fatura ürün pivot table oluşturma.
	2.	Birliktelik kurallarını oluşturma.

Görev 3: Sepet İçerisindeki Ürün ID’leri Verilen Kullanıcılara Ürün Önerisinde Bulunma

	1.	Verilen ürünlerin isimlerini bulma.
	2.	Ürün önerisinde bulunma.

