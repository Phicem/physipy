from ipywidgets import Layout
from traitlets import TraitError
from physipy import quantify, Dimension, Quantity, units, set_favunit, DimensionError
import ipywidgets as ipyw
import traitlets
from numpy import pi


class QuantityText(ipyw.Box, ipyw.ValueWidget, ipyw.DOMWidget):
    # dimension trait : a Dimension instance
    dimension = traitlets.Instance(Dimension, allow_none=False)
    # value trait : a Quantity instance
    value = traitlets.Instance(Quantity, allow_none=False)
    # value_number : float value of quantity
    value_number = traitlets.Float(allow_none=True)
    # string trait text
    display_val = traitlets.Unicode(allow_none=True)
    # description
    description = traitlets.Unicode(allow_none=True)
    
    def __init__(self, value=0.0, disabled=False, 
                 continuous_update=True, description="Quantity:",
                 fixed_dimension=False, placeholder="Type python expr",
                 **kwargs):
        
        # context for parsing
        self.context = {**units, "pi":pi}
        self.description = description
        
        # quantity work
        # set dimension
        value = quantify(value)
        self.dimension = value.dimension
        # if true, any change in value must have same dimension as initial dimension
        self.fixed_dimension = fixed_dimension
        
        # set quantity
        self.value = value
        # set text widget
        self.text = ipyw.Text(value=str(self.value),
                              placeholder=placeholder,
                              description=self.description,#'Set to:',
                              disabled=disabled,
                              continuous_update=continuous_update,
                              layout=Layout(width='auto',
                                            margin="0px 0px 0px 0px",
                                            padding="0px 0px 0px 0px",
                                            border="solid gray"),
                             style={'description_width': '130px'})
        
        # link text value and display_val unicode trait
        traitlets.link((self.text, "value"), (self, "display_val"))
        super().__init__(**kwargs)
        self.children = [self.text]

        # on_submit observe
        def text_update_values(wdgt):
            # get expression entered
            expression = wdgt.value
            # eval expression with unit context
            try:
                res = eval(expression, self.context)
                res = quantify(res)
                # update quantity value
                self.value = res
                # update display_value
                self.display_val = str(self.value)
            except:
                self.display_val = str(self.value)
        self.text.on_submit(text_update_values)

    # update value_number and text on quantity value change
    @traitlets.observe("value")
    def _update_display_val(self, proposal):
        self.value_number = self.value.value
        self.dimension = self.value.dimension
        self.display_val = f'{str(self.value)}'

    @traitlets.validate('value')
    def _valid_value(self, proposal):
        if self.fixed_dimension and proposal['value'].dimension != self.dimension:
            raise TraitError('value and parity should be consistent')
        return proposal['value']
    

class FDQuantityText(QuantityText):
    
    def __init__(self, value=0.0, disabled=False, 
                 continuous_update=True, description="Quantity:", *args,
                 **kwargs):
        
        super().__init__(value=value, disabled=disabled,
                         continuous_update=continuous_update, 
                         description=description,
                         fixed_dimension=True, 
                         *args, 
                         **kwargs)




class QuantitySlider(ipyw.Box, ipyw.ValueWidget, ipyw.DOMWidget):
    # dimension trait : a Dimension instance
    dimension = traitlets.Instance(Dimension, allow_none=False)
    # value trait : a Quantity instance
    value = traitlets.Instance(Quantity, allow_none=False)
    qmin = traitlets.Instance(Quantity, allow_none=False)
    qmax = traitlets.Instance(Quantity, allow_none=False)
    qstep = traitlets.Instance(Quantity, allow_none=False)
    # value_number : float value of quantity
    value_number = traitlets.Float(allow_none=True)
    # description
    description = traitlets.Unicode(allow_none=True)
    
    def __init__(self, value=0.0, min=None, max=None, step=None, disabled=False, 
                 continuous_update=True, description="Quantity:",
                 fixed_dimension=False, #placeholder="Type python expr",
                 **kwargs):
        
        super().__init__(**kwargs)

        
        # context for parsing
        #self.context = {**units, "pi":pi}
        self.description = description
        
        # quantity work
        # set dimension
        value = quantify(value)
        self.dimension = value.dimension
        # if true, any change in value must have same dimension as initial dimension
        self.fixed_dimension = fixed_dimension
        
        # set quantity
        self.value = value
        

        if min is not None:
            qmin = quantify(min)
            if not qmin.dimension == self.value.dimension:
                raise DimensionError(qmin.dimension, self.value.dimension)
        else:
            qmin = Quantity(0.0, self.value.dimension)
        # max value
        if max is not None:
            qmax = quantify(max)
            if not qmax.dimension == self.value.dimension:
                raise DimensionError(qmax.dimension, self.value.dimension)
        else:
            qmax = Quantity(100.0, self.value.dimension)        
        # step value
        if step is not None:
            qstep = quantify(step)
            if not qstep.dimension == self.value.dimension:
                raise DimensionError(qstep.dimension, self.value.dimension)
        else:
            qstep = Quantity(0.1, self.value.dimension)     
        
        self.qstep = qstep
        self.qmin = qmin
        self.qmax = qmax
        
        # set text widget
        self.slider = ipyw.FloatSlider(value=self.value.value,
                                       min=self.qmin.value,
                                       max=self.qmax.value,
                                       step=self.qstep.value,
                                       description=description,
                                       disabled=disabled,
                                       continuous_update=continuous_update,
                                       #orientation=orientation,
                                       readout=False,  # to disable displaying readout value
                                       #readout_format=readout_format,
                                       #layout=Layout(width="50%",
                                       #              margin="0px",
                                       #              border="solid red"),
                                      )
    
        def update_label_on_slider_change(change):
            self.value = Quantity(change.new, self.value.dimension, favunit=self.value.favunit)
            self.label.value = str(self.value)
        self.slider.observe(update_label_on_slider_change, names="value")
    
    
        # display the quantity value of the slider in label
        self.label = ipyw.Label(value=str(self.value))
        
        self.children = [
            self.slider,
            self.label,
        ]











        

def ui_widget_decorate(inits_values):
    """
    inits_values contains list of tuples : 
     - quantity init value
     - str description
     - name from signature
     
     Example
     -------
     def disk_PSA_cart(x, y, R, h):
         return x*y*R/h
     
     ui = ui_widget_decorate([("x", 1*m),
                              ("y", 1*m),
                              ("R", 1*m, "Radius"),
                              ("h", 1*m, "distance")])(disk_PSA_carth)
     
     """

    def decorator_func(func):
        
        # create a widget list for all inputs
        qwidget_list = []
        for initq in inits_values:
            # if provided, use alias for param
            if len(initq) == 3:
                qwidget_list.append(QuantityText(initq[1], description=initq[2]))
            # else use param name
            else:
                qwidget_list.append(QuantityText(initq[1], description=initq[0]))
                
        # wrap function to display result
        def display_func(*args, **kwargs):
            res = func(*args, **kwargs)
            display(res)
            return res

        # wrap all inputs widgets in a VBox
        input_ui = ipyw.VBox(qwidget_list)

        # create output widget, using inputs widgets
        out = ipyw.interactive_output(display_func,
                                     {k:qwidget_list[i] for i, k in enumerate([l[0] for l in inits_values])})

        # if func has a "name" attribute, create a Label for display, else use default function __name__
        if hasattr(func, "name"):
            wlabel = ipyw.Label(func.name)
        else:
            wlabel = ipyw.Label(func.__name__)
            
        # if func has a "latex" attribute, append it to Label
        if hasattr(func, "latex"):
            wlabel = ipyw.HBox([wlabel, ipyw.Label(func.latex)])
            
        # wrap all ui with Labels, inputs, and result
        ui = ipyw.VBox([wlabel, input_ui, out])

        return ui        
    return decorator_func
    
    
    

            
        
def ui_widget_decorate_from_annotations(func):
    """
     Example
     -------
     def disk_PSA_cart(x:mm, y:mm, R:mm, h:mm)-> msr:
         return x*y*R/h
     
     ui = ui_widget_decorate_from_annotations(disk_PSA_carth)
     ui

     """
    
    # recreating an inits_values list based on annotations
    # then reusing ui_widget_decorate
    
    import inspect
    sig = inspect.signature(func)
    inits_values = []
    
    for k,v in sig.parameters.items():
        inits_values.append((v.name, v.annotation, v.name))

    # fyi : to get retun annotation
    #sig.return_annotation
    if not sig.return_annotation == inspect._empty:
        func = set_favunit(sig.return_annotation)(func)
    
    return ui_widget_decorate(inits_values)(func)
            
    
def FunctionUI(tab_name, function_dict):
    acc = ipyw.Accordion()
    
    sections_uis = []
    i = 0
    for section_name, section_functions_list in function_dict.items():
        function_uis = []
        # loop over all functions in section and generate ui
        for func in section_functions_list:
            ui = ui_widget_decorate_from_annotations(func)
            function_uis.append(ui)
        box = ipyw.VBox(function_uis)
        sections_uis.append(box)
        acc.set_title(i, section_name)
        i+=1
        
    acc.children = sections_uis

    
    
    tab = ipyw.Tab()
    tab.children = [acc]
    tab.set_title(0, tab_name)

    return tab