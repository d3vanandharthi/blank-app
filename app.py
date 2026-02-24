# This is Mini Project - for User App using DynamoDB.
#Libraries
import streamlit as st
import boto3
import uuid #UUID library to generate unique user IDs
from botocore.exceptions import ClientError
 
#------AWS Configuration--------------
REGION = 'us-east-1'
TABLE_NAME = 'UserTable'
#-------------------------------------
 
#Initilize DynamoDB resource
try:
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(TABLE_NAME)
 
except Exception as e:
    st.error(f"Error initializing/Connecting to  DynamoDB: {e}")
    st.stop()
 
#--------- UI ------------------
st.title("User Management App with DynamoDB")
st.subheader("Add New User")
name = st.text_input("Name")
email = st.text_input("Email")
 
if st.button("Submitt User"):
    if name and email:
        try:
            user_id = str(uuid.uuid4()) # Generate unique user ID
            table.put_item(Item={
                'id': user_id,  # Use 'ID' as the primary key in DynamoDB
                'Name': name,   # Use 'Name' as the attribute for the user's name
                'Email': email}) # Use 'Email' as the attribute for the user's email
            st.success(f"User {name} added successfully with ID: {user_id}")    
        except ClientError as e:
            st.error(f"Error adding user: {e.response['Error']['Message']}")    
    else:
        st.warning("Please enter both name and email to add a user/Fill all details.")
 
st.divider()    #UI Divider
 
st.subheader("View ALL Users")
if st.button("Load/Fetch Users"):
    try:
        response = table.scan() # Scan the DynamoDB table to get all items
        items = response.get('Items', [])
 
        if items:
            st.dataframe(items) # Display the items in a table format using Streamlit
        else:
            st.info("No users found in the database.")
    except ClientError as e:
        st.error(f"Error fetching users: {e.response['Error']['Message']}")