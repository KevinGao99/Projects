#!/usr/bin/env python
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from datetime import datetime
from collections import Counter

def get_data():
    return pd.read_csv('https://raw.githubusercontent.com/KevinGao99/Projects/main/Github_Dataset/Data/github_dataset.csv')


df = get_data()
df.fillna('Not Specified', inplace=True)


# Repository Popularity Overview: Bar charts to display repositories with the highest stars and forks.
# st.bar_chart(data = df1,\
#     x = 'repositories',\
#     y = st.session_state['category'],\
#         color = '#0361ff')
# st.set_page_config(layout = 'wide')
st.markdown('''
<style>
.big-font {
    font-size:28px !important;
}
</style>
''', unsafe_allow_html= True)
st.markdown('<p class="big-font">Github Repository Popularity Overview</p>', unsafe_allow_html=True)

if 'bar_num' not in st.session_state:
    st.session_state['bar_num'] = 10
if 'category' not in st.session_state:
    st.session_state['category'] = 'stars_count'
bn1 = st.selectbox(label = 'Select the number of repositories to display',\
    options = [5, 10, 15])
st.session_state['bar_num'] = bn1
bc1 = st.selectbox(label = 'Select the category to display',\
    options = ['stars_count', 'forks_count'])
st.session_state['category'] = bc1

df1 = df.sort_values(by = st.session_state['category'], ascending = False)[:st.session_state['bar_num'] + 1].reset_index().drop('index', axis = 1)
st.write('The following bar chart shows the top ', st.session_state['bar_num'], ' repositories with the highest ', st.session_state['category'], ' on Github.')
st.write(alt.Chart(df1).mark_bar().encode(
    y = alt.Y('repositories:N', sort = '-x'),
    x = alt.X(st.session_state['category']+':Q', axis = alt.Axis(tickSize = 0)),
    tooltip = [
        alt.Tooltip('repositories:N', title = 'Repository'),
        alt.Tooltip(st.session_state['category']+':Q', title = st.session_state['category'].replace('_', ' ').title())
    ],
    text = st.session_state['category'],
).properties(width = 800, height = 600).configure_mark(color = '#0361ff').interactive())

# Language Distribution: Bar charts to show the breakdown of primary languages used in the repositories.
st.markdown('<p class="big-font">Github Repository Language Distribution</p>', unsafe_allow_html=True)
df3 = df.groupby('language').count().reset_index().sort_values(by = 'repositories', ascending = False)
df3.rename(columns = {'repositories':'count'}, inplace = True)
st.write(alt.Chart(data = df3).mark_bar().encode(
    x = alt.X('count:Q'),
    y = alt.Y('language:N', sort = '-x'),
    tooltip = [
        alt.Tooltip('language:N', title = 'Language'),
        alt.Tooltip('count:Q', title = 'Count')
    ]
).properties(width = 800, height = 600).configure_mark(color = '#0361ff').interactive())

# Calculate the Language using frequency for users
st.markdown('<p class="big-font">Github Repository Language Frequency</p>', unsafe_allow_html=True)
df10 = df.groupby('language').sum().reset_index().sort_values(by = 'contributors', ascending = False)
df10.rename(columns = {'contributors':'count'}, inplace = True)
st.write(alt.Chart(df10).mark_bar().encode(
    x = alt.X('count:Q'),
    y = alt.Y('language:N', sort = '-x'),
    tooltip = [
        alt.Tooltip('language:N', title = 'Language'),
        alt.Tooltip('count:Q', title = 'Contributor Count')
    ]
).properties(width = 800, height = 600).configure_mark(color = '#0361ff').interactive())

# Activity and Engagement Metrics: Scatter charts to monitor issues and pull requests over time.
st.markdown('<p class="big-font">Github Repository Activity Overview for Different Languages</p>', unsafe_allow_html=True)
if['lang_issue'] not in st.session_state:
    st.session_state['lang_issue'] = 'Python'
lang_issue = st.selectbox(label = 'Select the programming language to display',\
                          options = df['language'].unique())
st.session_state['lang_issue'] = lang_issue
df2 = df[df['language'] == st.session_state['lang_issue']]
# st.scatter_chart(data = df2,
#                     x = 'issues_count',
#                     y = 'pull_requests',
#                     color = '#0361ff', height = 600,
#                     width = 800, size = 25)

# alt2 = alt.Chart(df2).mark_circle(size = 30).encode(
#     x = 'issues_count',
#     y = 'pull_requests',
#     tooltip = [
#         alt.Tooltip('repositories:N', title = 'Repository'),
#         alt.Tooltip('issues_count:Q', title = 'Issues'),
#         alt.Tooltip('pull_requests:Q', title = 'Pull Requests')
#     ]
# )
# alt2.porperties(width = 800, height = 600).configure_mark(color = '#0361ff')
st.write(alt.Chart(df2).mark_circle(size = 30).encode(
    x = 'issues_count',
    y = 'pull_requests',
    tooltip = [
        alt.Tooltip('repositories:N', title = 'Repository'),
        alt.Tooltip('issues_count:Q', title = 'Issues'),
        alt.Tooltip('pull_requests:Q', title = 'Pull Requests')
    ]
).properties(width = 800, height = 600).configure_mark(color = '#0361ff').interactive()
)

# Contributor Engagement: Scatter plots to analyze the correlation between the number of contributors and repository popularity.
st.markdown('<p class="big-font">Github Repository Contributor Engagement</p>', unsafe_allow_html=True)
df4 = df.groupby('repositories').sum().reset_index().sort_values(by = 'contributors', ascending = False)[['repositories', 'contributors']]
df4.rename(columns = {'contributors':'contributor_count'}, inplace = True)
df5 = df.groupby('repositories').sum().reset_index().sort_values(by = 'stars_count', ascending = False)[['repositories', 'stars_count', 'forks_count']]
df6 = pd.merge(df4, df5, on = 'repositories')
df7 = df6.copy(deep = True)[['repositories', 'contributor_count', 'stars_count']]
df7.rename(columns = {'stars_count':'count'}, inplace = True)
df7['label'] = 'Stars'
df8 = df6.copy(deep = True)[['repositories', 'contributor_count', 'forks_count']]
df8.rename(columns = {'forks_count':'count'}, inplace = True)
df8['label'] = 'Forks'
df9 = pd.concat([df7, df8])
df9['count'] = df9['count'] + 1
st.write(alt.Chart(df9).mark_circle(size = 20).encode(
    x = alt.X('contributor_count'),
    y = alt.Y('count').scale(alt.Scale(type = 'log')),
    tooltip = [
        alt.Tooltip('repositories:N', title = 'Repository'),
        alt.Tooltip('contributor_count:Q', title = 'Contributors'),
        alt.Tooltip('count:Q', title = 'Count'),
        alt.Tooltip('label:N', title = 'Label')
    ],
    color = 'label:N'
).properties(width = 800, height = 600).configure_mark(color = '#0361ff').interactive())
