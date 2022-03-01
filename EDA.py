import numpy as np
import scipy as sp
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Plotting options
#%matplotlib inline
mpl.style.use('ggplot')
sns.set(style='whitegrid')

class EDA:
    def __init__(self, loans):
        self.loans = loans
        
    def plot_var(self, col_name, full_name, continuous):
        """
        Visualize a variable with and without faceting on the loan status.
        - col_name is the variable name in the dataframe
        - full_name is the full variable name
        - continuous is True if the variable is continuous, False otherwise
        """
        f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12,3), dpi=90)

        # Plot without loan status
        if continuous:
            sns.distplot(self.loans.loc[self.loans[col_name].notnull(), col_name], kde=False, ax=ax1)
        else:
            sns.countplot(self.loans[col_name], order=sorted(self.loans[col_name].unique()), color='#5975A4', saturation=1, ax=ax1)
        ax1.set_xlabel(full_name)
        ax1.set_ylabel('Count')
        ax1.set_title(full_name)

        # Plot with loan category
        if continuous:
            sns.boxplot(x=col_name, y='loan_category', data=self.loans, ax=ax2)
            ax2.set_ylabel('')
            ax2.set_title(full_name + ' by Loan Category')
        else:
            charge_off_rates = self.loans.groupby(col_name)['loan_category'].value_counts(normalize=True).loc[:,'bad']
            sns.barplot(x=charge_off_rates.index, y=charge_off_rates.values, color='#5975A4', saturation=1, ax=ax2)
            ax2.set_ylabel('Fraction of Bad Loans')
            ax2.set_title('Bad Loans Rate by ' + full_name)
        ax2.set_xlabel(full_name)

        plt.tight_layout()
        
    def plot_countplot(self, col_name):
        '''
        Countplot for categorical variables
        '''
        f, axes = plt.subplots(ncols=3,figsize=(17,6))

        a0 = sns.countplot(self.loans[col_name],label="Count", order = self.loans[col_name].value_counts().index,ax=axes[0])
        a0.set_xticklabels(labels= list(self.loans[col_name].value_counts().index),rotation=90)
        a0.set_title("Countplot for All")
        for p in a0.patches:
            a0.annotate(format(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')

        loans_0 = self.loans[self.loans['loan_category']=='bad']
        a1 = sns.countplot(loans_0[col_name],label="Count",order = self.loans[col_name].value_counts().index, ax=axes[1])
        a1.set_xticklabels(labels= list(self.loans[col_name].value_counts().index),rotation=90)
        a1.set_title("Countplot for bad loans")
        for p in a1.patches:
            a1.annotate(format(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')

        loans_1 = self.loans[self.loans['loan_category']=='good']
        a2 = sns.countplot(loans_1[col_name],label="Count",order = self.loans[col_name].value_counts().index, ax=axes[2])
        a2.set_xticklabels(labels= list(self.loans[col_name].value_counts().index),rotation=90)
        a2.set_title("Countplot for good loans")
        for p in a2.patches:
            a2.annotate(format(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
            
    def plot_density_plot(self, col_name):
#     f, axes = plt.subplots(ncols=2,figsize=(17,6))

#     sns.distplot(loans[loans['loan_category'] == 'bad'][col_name],label='0',bins=30,ax=axes[0])
#     sns.distplot(loans[loans['loan_category'] == 'good'][col_name],label='1',bins=30,ax=axes[0])
#     plt.legend(title='loan_category',loc='best')

#     sns.kdeplot(loans.loc[loans['loan_category'] == 'bad', col_name], label = 'bad-loan',shade=True,ax=axes[1])
#     sns.kdeplot(loans.loc[loans['loan_category'] == 'good', col_name], label = 'good-loan',shade=True,ax=axes[1])
#     plt.xlabel(col_name); plt.ylabel('Density')
    
        sns.kdeplot(self.loans.loc[self.loans['loan_category'] == 'bad', col_name], label = 'bad-loan',shade=True)
        sns.kdeplot(self.loans.loc[self.loans['loan_category'] == 'good', col_name], label = 'good-loan',shade=True)
        plt.xlabel(col_name)
        plt.ylabel('Density')
        plt.legend()