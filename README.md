# ClickSoftware FSE Remove RelocatedResources Automatically
How to automate the complete deletion of objects with error exceptions in ClickSoftware FSE object services API.

<h3>Description</h3>
<p>
The <a href="https://wiki.cloud.clicksoftware.com/fsedoc/en/development/service-edge-api-references/rest-api-reference/object-services-rest-apis">ClickSoftware FSE Object Services API</a> 
  is a RESTful API that allows developers to GET, UPDATE, or DELETE database records in the ClickSoftware FSE system. If the developer is attempting to delete a record the 
  Object service API returns error code 500 and error messages that contain references to the foreign key restraint that is causing the error. The purpose of sharing this public
  Git repo is to share how you can perform first and second string parsing of dynamic key references to recursively remove a relocated resource object from ClickSoftware FSE.
</p>

<h3>Problem</h3>
<p>
  The goal is to delete relocated resource Pete Herrera, Substation Maintenance, Sub Crews. When trying to delete Pete's relocated resource, I'm getting HTTP error code
  500 with the response message: "Cannot delete Engineer Pete Herrera Substation Maintenance, Area Heads (key=817496064) as it is referenced by attribute RequiredEngineers of Task  11108649-0120 (key=1800617986)".
  To remove this key constraint, I must remove the Task's (CallID 11108649-0120 (key=1800617986)) RequiredEngineer field value. RequiredEngineer dataType is a list so to
  remove the required engineer, I have to pass an empty array to the Update Object service API. Now I'm able to delete the relocated resource HOWEVER, there's now different tasks
  associated to Pete Herrera, Substation Maintenance. The total count of RequiredEngineer associations are up to the ten thousands!!!! 😭. 
</p>

<h3>Conceptual Walkthrough</h3>
<ol>
  <li>Use Click's Object Service API to Delete Relocated Engineer by Key</li>
  <li>If Successful, return success! because the relocated engineer is deleted</li>
  <li>Otherwise, if status code 500, parse the exception message by requiredEngineers and then by (key=</li>
  <li>Update the task that's causing the requiredEngineers's key restraint</li>
  <li>Try to delete the relocated engineer by key again</li>
  <li>Keep doing this recursively until the relocated engineer object is deleted</li>
</ol>
