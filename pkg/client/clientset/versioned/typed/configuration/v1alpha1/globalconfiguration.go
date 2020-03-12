// Code generated by client-gen. DO NOT EDIT.

package v1alpha1

import (
	"time"

	v1alpha1 "github.com/nginxinc/kubernetes-ingress/pkg/apis/configuration/v1alpha1"
	scheme "github.com/nginxinc/kubernetes-ingress/pkg/client/clientset/versioned/scheme"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	types "k8s.io/apimachinery/pkg/types"
	watch "k8s.io/apimachinery/pkg/watch"
	rest "k8s.io/client-go/rest"
)

// GlobalConfigurationsGetter has a method to return a GlobalConfigurationInterface.
// A group's client should implement this interface.
type GlobalConfigurationsGetter interface {
	GlobalConfigurations(namespace string) GlobalConfigurationInterface
}

// GlobalConfigurationInterface has methods to work with GlobalConfiguration resources.
type GlobalConfigurationInterface interface {
	Create(*v1alpha1.GlobalConfiguration) (*v1alpha1.GlobalConfiguration, error)
	Update(*v1alpha1.GlobalConfiguration) (*v1alpha1.GlobalConfiguration, error)
	Delete(name string, options *v1.DeleteOptions) error
	DeleteCollection(options *v1.DeleteOptions, listOptions v1.ListOptions) error
	Get(name string, options v1.GetOptions) (*v1alpha1.GlobalConfiguration, error)
	List(opts v1.ListOptions) (*v1alpha1.GlobalConfigurationList, error)
	Watch(opts v1.ListOptions) (watch.Interface, error)
	Patch(name string, pt types.PatchType, data []byte, subresources ...string) (result *v1alpha1.GlobalConfiguration, err error)
	GlobalConfigurationExpansion
}

// globalConfigurations implements GlobalConfigurationInterface
type globalConfigurations struct {
	client rest.Interface
	ns     string
}

// newGlobalConfigurations returns a GlobalConfigurations
func newGlobalConfigurations(c *K8sV1alpha1Client, namespace string) *globalConfigurations {
	return &globalConfigurations{
		client: c.RESTClient(),
		ns:     namespace,
	}
}

// Get takes name of the globalConfiguration, and returns the corresponding globalConfiguration object, and an error if there is any.
func (c *globalConfigurations) Get(name string, options v1.GetOptions) (result *v1alpha1.GlobalConfiguration, err error) {
	result = &v1alpha1.GlobalConfiguration{}
	err = c.client.Get().
		Namespace(c.ns).
		Resource("globalconfigurations").
		Name(name).
		VersionedParams(&options, scheme.ParameterCodec).
		Do().
		Into(result)
	return
}

// List takes label and field selectors, and returns the list of GlobalConfigurations that match those selectors.
func (c *globalConfigurations) List(opts v1.ListOptions) (result *v1alpha1.GlobalConfigurationList, err error) {
	var timeout time.Duration
	if opts.TimeoutSeconds != nil {
		timeout = time.Duration(*opts.TimeoutSeconds) * time.Second
	}
	result = &v1alpha1.GlobalConfigurationList{}
	err = c.client.Get().
		Namespace(c.ns).
		Resource("globalconfigurations").
		VersionedParams(&opts, scheme.ParameterCodec).
		Timeout(timeout).
		Do().
		Into(result)
	return
}

// Watch returns a watch.Interface that watches the requested globalConfigurations.
func (c *globalConfigurations) Watch(opts v1.ListOptions) (watch.Interface, error) {
	var timeout time.Duration
	if opts.TimeoutSeconds != nil {
		timeout = time.Duration(*opts.TimeoutSeconds) * time.Second
	}
	opts.Watch = true
	return c.client.Get().
		Namespace(c.ns).
		Resource("globalconfigurations").
		VersionedParams(&opts, scheme.ParameterCodec).
		Timeout(timeout).
		Watch()
}

// Create takes the representation of a globalConfiguration and creates it.  Returns the server's representation of the globalConfiguration, and an error, if there is any.
func (c *globalConfigurations) Create(globalConfiguration *v1alpha1.GlobalConfiguration) (result *v1alpha1.GlobalConfiguration, err error) {
	result = &v1alpha1.GlobalConfiguration{}
	err = c.client.Post().
		Namespace(c.ns).
		Resource("globalconfigurations").
		Body(globalConfiguration).
		Do().
		Into(result)
	return
}

// Update takes the representation of a globalConfiguration and updates it. Returns the server's representation of the globalConfiguration, and an error, if there is any.
func (c *globalConfigurations) Update(globalConfiguration *v1alpha1.GlobalConfiguration) (result *v1alpha1.GlobalConfiguration, err error) {
	result = &v1alpha1.GlobalConfiguration{}
	err = c.client.Put().
		Namespace(c.ns).
		Resource("globalconfigurations").
		Name(globalConfiguration.Name).
		Body(globalConfiguration).
		Do().
		Into(result)
	return
}

// Delete takes name of the globalConfiguration and deletes it. Returns an error if one occurs.
func (c *globalConfigurations) Delete(name string, options *v1.DeleteOptions) error {
	return c.client.Delete().
		Namespace(c.ns).
		Resource("globalconfigurations").
		Name(name).
		Body(options).
		Do().
		Error()
}

// DeleteCollection deletes a collection of objects.
func (c *globalConfigurations) DeleteCollection(options *v1.DeleteOptions, listOptions v1.ListOptions) error {
	var timeout time.Duration
	if listOptions.TimeoutSeconds != nil {
		timeout = time.Duration(*listOptions.TimeoutSeconds) * time.Second
	}
	return c.client.Delete().
		Namespace(c.ns).
		Resource("globalconfigurations").
		VersionedParams(&listOptions, scheme.ParameterCodec).
		Timeout(timeout).
		Body(options).
		Do().
		Error()
}

// Patch applies the patch and returns the patched globalConfiguration.
func (c *globalConfigurations) Patch(name string, pt types.PatchType, data []byte, subresources ...string) (result *v1alpha1.GlobalConfiguration, err error) {
	result = &v1alpha1.GlobalConfiguration{}
	err = c.client.Patch(pt).
		Namespace(c.ns).
		Resource("globalconfigurations").
		SubResource(subresources...).
		Name(name).
		Body(data).
		Do().
		Into(result)
	return
}