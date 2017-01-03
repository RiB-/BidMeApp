"""
Created on Thu, Sept 24th, 2015

Author: Romano
"""

def MVP_ShowP(fromUser  = 'Default'):

	#%%******************************************************************************
	# Importing packages
	#******************************************************************************
	import pandas as pd  #library for advanced data analysis
	import pickle
	#******************************************************************************

	Input_Model_Path = 'model/'
	Input_Path_Man = 'model/'
	GT_Feat_LR_SIM_DF = pd.read_pickle(Input_Model_Path + 'GT_Feat_LR_SIM_DF.pkl')	
	Prod_Info_DF = pd.read_pickle(Input_Path_Man + 'Prod_Info_DF.pkl')

	Gen_Pred_Prod = GT_Feat_LR_SIM_DF.sample(n=1)

	Gen_Pred_Prod.to_pickle(Input_Model_Path + 'Gen_Pred_Prod.pkl')

	Gen_Pred_Prod = Gen_Pred_Prod.drop(['Offer_Status'], axis=1)
	Category_Mapping = pickle.load(open(Input_Path_Man + 'Category_Mapping.p', "rb" ) )
	Inv_Category_Mapping = {v: k for k, v in Category_Mapping.items()}
	Show_DF = Gen_Pred_Prod.copy()
	Show_DF['Product_Category'] = Show_DF['Product_Category'].replace(Inv_Category_Mapping)

	Product_Name = Prod_Info_DF['Products Name'].values[0]
	Brand = Prod_Info_DF['Brand'].values[0]
	Category = Show_DF['Product_Category'].values[0]
	Avg_Ret_Price = float("{0:.2f}".format(Show_DF['Avg_Ret_Price'].values[0]))
	Min_Sale_Price = float("{0:.2f}".format(Show_DF['Min_Sale_Price'].values[0]))

	Savelist = [Product_Name, Brand, Category, Avg_Ret_Price, Min_Sale_Price]

	with open(Input_Path_Man + 'Savelist.p', 'wb') as f:
	    pickle.dump(Savelist, f)
	#end

	return Product_Name, Brand, Category, Avg_Ret_Price, Min_Sale_Price
#end

def MVP_Result(fromUser  = 'Default', User_Offer = 0):

	#%%******************************************************************************
	# Importing packages
	#******************************************************************************
	import pandas as pd  #library for advanced data analysis
	import pickle
	#******************************************************************************
	Input_Model_Path = 'model/'
	Input_Path_Man = 'model/'

	with open(Input_Model_Path + 'LogReg_obj.pkl','r') as f:
	    LogReg_obj = pickle.load(f)
	#end

	GT_Feat_LR_SIM_DF = pd.read_pickle(Input_Model_Path + 'GT_Feat_LR_SIM_DF.pkl')

	Model_ID = 'Ratio'

	#******************************************************************************
	# Predicting
	#******************************************************************************
	Gen_Pred_Prod =pd.read_pickle(Input_Model_Path + 'Gen_Pred_Prod.pkl')
	Gen_Pred_Prod = Gen_Pred_Prod.drop(['Offer_Status'], axis=1)
	Category_Mapping = pickle.load(open(Input_Path_Man + 'Category_Mapping.p', "rb" ) )
	Inv_Category_Mapping = {v: k for k, v in Category_Mapping.items()}

	if Model_ID=='Simple':
	    Gen_Pred_Prod['Offer_Price'] = User_Offer
	#end
	if Model_ID=='Ratio':
	    Gen_Pred_Prod['Offer_Price'] = 1.0*User_Offer/Gen_Pred_Prod['Avg_Ret_Price']
	#end

	Pred_Array_Imp = Gen_Pred_Prod.values

	Predictions = LogReg_obj.predict(Pred_Array_Imp).astype(int) #make predictions from trained algoritm using the test data
	Pred_Probability = LogReg_obj.predict_proba(Pred_Array_Imp)

	Proba_out = float("{0:.2f}".format(Pred_Probability[0,1]))

	return Proba_out

	# if fromUser != 'Default':
	# 	return Proba_out
	# else:
	# 	return 'Check your Input'
	#end
#end

def GetCatList():
	import pickle
	import pandas as pd
	Input_Path_Man = 'model/'
	Prod_Info_Unique_DF = pd.read_pickle(Input_Path_Man + 'Prod_Info_Unique_DF.pkl')
	Category_List = Prod_Info_Unique_DF['Product Category'].unique().tolist()
	return Category_List
#end

def GetSubcatList(Category):
	import pickle
	import pandas as pd
	Input_Path_Man = 'model/'
	Prod_Info_Unique_DF = pd.read_pickle(Input_Path_Man + 'Prod_Info_Unique_DF.pkl')

	with open(Input_Path_Man + 'Category.p','wb') as f:
	    pickle.dump(Category, f)
	#end

	Subcategory_List = Prod_Info_Unique_DF['Subcategory'][Prod_Info_Unique_DF['Product Category']==Category].unique().tolist()
	return Subcategory_List
#end

def GetBrandList(Subcategory):
	import pickle
	import pandas as pd
	Input_Path_Man = 'model/'
	Prod_Info_Unique_DF = pd.read_pickle(Input_Path_Man + 'Prod_Info_Unique_DF.pkl')

	with open(Input_Path_Man + 'Category.p','r') as f:
	    Category = str(pickle.load(f))
	#end	

	with open(Input_Path_Man + 'Subcategory.p','wb') as f:
	    pickle.dump(Subcategory, f)
	#end

	Brand_List = Prod_Info_Unique_DF['Brand'][Prod_Info_Unique_DF['Subcategory']==Subcategory][Prod_Info_Unique_DF['Product Category']==Category].unique().tolist()
	return Category, Brand_List
#end

def GetProdList(Brand):
	import pickle
	import pandas as pd
	Input_Path_Man = 'model/'
	Prod_Info_Unique_DF = pd.read_pickle(Input_Path_Man + 'Prod_Info_Unique_DF.pkl')

	with open(Input_Path_Man + 'Category.p','r') as f:
	    Category = str(pickle.load(f))
	#end	
	with open(Input_Path_Man + 'Subcategory.p','r') as f:
	    Subcategory = str(pickle.load(f))
	#end	

	with open(Input_Path_Man + 'Brand.p','wb') as f:
	    pickle.dump(Brand, f)
	#end

	Prod_List = Prod_Info_Unique_DF['Products Name'][Prod_Info_Unique_DF['Brand']==Brand][Prod_Info_Unique_DF['Subcategory']==Subcategory][Prod_Info_Unique_DF['Product Category']==Category].unique().tolist()
	return Category, Subcategory, Prod_List
#end

def GetProdID(Product):
	import pickle
	import pandas as pd
	Input_Path_Man = 'model/'
	Prod_Info_Unique_DF = pd.read_pickle(Input_Path_Man + 'Prod_Info_Unique_DF.pkl')

	with open(Input_Path_Man + 'Category.p','r') as f:
	    Category = str(pickle.load(f))
	#end	
	with open(Input_Path_Man + 'Subcategory.p','r') as f:
	    Subcategory = str(pickle.load(f))
	#end	
	with open(Input_Path_Man + 'Brand.p','r') as f:
	    Brand = str(pickle.load(f))
	#end

	Prod_ID = str(Prod_Info_Unique_DF['Prod_ID'][Prod_Info_Unique_DF['Products Name']==Product][Prod_Info_Unique_DF['Brand']==Brand][Prod_Info_Unique_DF['Subcategory']==Subcategory][Prod_Info_Unique_DF['Product Category']==Category].tolist()[0])

	return Category, Subcategory, Brand, Prod_ID
#end

def GetPriceInfo(Prod_ID):
	import pickle
	import pandas as pd
	Input_Model_Path = 'model/'
	Full_CatFeat_SIM_01_DF = pd.read_pickle(Input_Model_Path + 'Full_CatFeat_SIM_01_DF.pkl')

	Avg_Ret_Price = float("{0:.2f}".format(Full_CatFeat_SIM_01_DF['Avg_Ret_Price'][Full_CatFeat_SIM_01_DF['Prod_ID']==Prod_ID].values[0]))
	Min_Sale_Price = float("{0:.2f}".format(Full_CatFeat_SIM_01_DF['Min_Sale_Price'][Full_CatFeat_SIM_01_DF['Prod_ID']==Prod_ID].values[0]))

	return Avg_Ret_Price, Min_Sale_Price
#end

def Predicting(Pred_Obj, Feat_DF, Prod_ID, User_Offer, Drop_Feat = 'None', Model_ID = 'Ratio', Standardize = 'False'):

	if Drop_Feat=='None':
		Drop_Feat = ['Prod_ID','Offer_Status']
	#end

	#--------------------------------
	# Define the path
	#--------------------------------
	Input_Path_Man = 'model/'
	#--------------------------------
	Feat_DF = Feat_DF.drop(Drop_Feat, axis=1)

	if Model_ID=='Simple':
	    Feat_DF['Offer_Price'] = User_Offer
	#end
	if Model_ID=='Ratio':
	    Feat_DF['Offer_Price'] = 1.0*User_Offer/Feat_DF['Min_Sale_Price']
	#end

	if User_Offer>=Feat_DF['Avg_Ret_Price'].values[0]:
		Pred_Probability = [[0.01, 0.98, 0.01]]
	else:
		Pred_Array_Imp = Feat_DF.values

		#%%
		if Standardize == 'True': #if standardization of the predictor features is required
		    Pred_Array_Imp_Stand = Scaler.transform(Pred_Array_Imp) #standardize the dataset for predictions
		#end

		if Standardize == 'True': #if standardization of the predictor features is required
		    Predictions = Pred_Obj.predict(Pred_Array_Imp_Stand).astype(int) #make predictions from trained algoritm using the test data
		    Pred_Probability = Pred_Obj.predict_proba(Pred_Array_Imp_Stand)
		else:
		    Predictions = Pred_Obj.predict(Pred_Array_Imp).astype(int) #make predictions from trained algoritm using the test data
		    Pred_Probability = Pred_Obj.predict_proba(Pred_Array_Imp)
		#end

	#end

	return float("{0:.2f}".format(Pred_Probability[0][1])), float("{0:.2f}".format(Pred_Probability[0][2]))

#end

