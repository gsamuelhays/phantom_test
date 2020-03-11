"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
##############################
# Start - Global Code Block

from decimal import Decimal

# End - Global Code block
##############################

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'decision_2' block
    decision_2(container=container)

    return

def post_answer_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('post_answer_1() called')

    find_answer__answer = json.loads(phantom.get_run_data(key='find_answer:answer'))
    source_data_identifier_value = container.get('source_data_identifier', None)

    # collect data for 'post_answer_1' call

    parameters = []
    
    # build parameters list for 'post_answer_1' call
    parameters.append({
        'answer': find_answer__answer,
        'r_id': source_data_identifier_value,
    })

    phantom.act("post answer", parameters=parameters, assets=['autobots'], callback=decision_1, name="post_answer_1")

    return

def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('decision_1() called')

    # check for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["post_answer_1:action_result.data.*.status", "==", "CORRECT"],
        ])

    # call connected blocks if condition 1 matched
    if matched_artifacts_1 or matched_results_1:
        set_status_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # call connected blocks for 'else' condition 2
    promote_to_case_2(action=action, success=success, container=container, results=results, handle=handle)

    return

def set_status_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('set_status_1() called')

    phantom.set_status(container=container, status="Closed")

    return

def promote_to_case_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('promote_to_case_2() called')

    phantom.promote(container=container, template="Response Template 1")

    return

def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('decision_2() called')
    
    tags_value = container.get('tags', None)

    # check for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["Array Processing", "in", tags_value],
        ])

    # call connected blocks if condition 1 matched
    if matched_artifacts_1 or matched_results_1:
        find_answer(action=action, success=success, container=container, results=results, handle=handle)
        return

    # call connected blocks for 'else' condition 2

    return

def find_answer(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('find_answer() called')
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.list', 'artifact:*.tags', 'artifact:*.id'])
    container_item_0 = [item[0] for item in container_data]
    container_item_1 = [item[1] for item in container_data]

    find_answer__answer = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    for i in container_item_1:
        phantom.debug("container1 = {}, i = {}".format(container_item_1, i))
        if i is not None and len(i) > 0:
            tag = i[0]
    for i in container_item_0:
        phantom.debug("container0 = {}, i = {}".format(container_item_0, i))
        if i is not None and len(i) > 0:
            the_list = i
    
    if tag == 'largest':
        find_answer__answer = max(the_list)
    elif tag == 'smallest':
        find_answer__answer = min(the_list)
    elif tag == 'sum':
        find_answer__answer = sum(the_list)
    elif tag == 'product':
        t = 1
        for i in the_list:
            t = t * i
        phantom.debug("answer = {}".format(t))
        phantom.debug("str(answer) = {}".format(str(t)))
        find_answer__answer = str(t)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key='find_answer:answer', value=json.dumps(find_answer__answer))
    post_answer_1(container=container)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return